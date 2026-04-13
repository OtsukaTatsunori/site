import { useState, useEffect } from 'react'
import AssetPicker from './components/AssetPicker'
import Preview from './components/Preview'
import './App.css'

function App() {
  const [text, setText] = useState('')
  const [scenes, setScenes] = useState([])
  const [loading, setLoading] = useState(false)
  const [globalSpeed, setGlobalSpeed] = useState(1.0)
  const [selectedSceneIdx, setSelectedSceneIdx] = useState(null)
  const [bgm, setBgm] = useState(null)
  const [bgmVolume, setBgmVolume] = useState(80)
  const [transition, setTransition] = useState('cut')
  const [aspectRatio, setAspectRatio] = useState('9:16')
  const [rendering, setRendering] = useState(false)
  const [renderResult, setRenderResult] = useState(null)

  // TTS関連
  const [ttsAvailable, setTtsAvailable] = useState(false)
  const [ttsSpeakers, setTtsSpeakers] = useState([])
  const [ttsSpeakerId, setTtsSpeakerId] = useState(1)
  const [ttsSpeed, setTtsSpeed] = useState(1.0)
  const [ttsGenerating, setTtsGenerating] = useState(false)
  const [showPreview, setShowPreview] = useState(false)

  // テンプレート関連
  const [templates, setTemplates] = useState([])
  const [showTemplateSave, setShowTemplateSave] = useState(false)
  const [templateName, setTemplateName] = useState('')

  // プロジェクト関連
  const [projects, setProjects] = useState([])
  const [currentProjectFile, setCurrentProjectFile] = useState(null)
  const [projectName, setProjectName] = useState('新規プロジェクト')
  const [showProjectList, setShowProjectList] = useState(false)

  // テンプレート一覧を読み込み
  const loadTemplates = () => {
    fetch('/api/templates')
      .then((res) => res.json())
      .then((data) => setTemplates(data.templates || []))
  }

  // プロジェクト一覧を読み込み
  const loadProjects = () => {
    fetch('/api/projects')
      .then((res) => res.json())
      .then((data) => setProjects(data.projects || []))
  }

  // TTS接続状態を確認
  useEffect(() => {
    loadTemplates()
    loadProjects()
    fetch('/api/tts/status')
      .then((res) => res.json())
      .then((data) => {
        setTtsAvailable(data.available)
        if (data.available) {
          fetch('/api/tts/speakers')
            .then((res) => res.json())
            .then((d) => setTtsSpeakers(d.speakers || []))
        }
      })
      .catch(() => setTtsAvailable(false))
  }, [])

  // テキストをシーンに自動分割
  const handleSplitText = async () => {
    if (!text.trim()) return
    setLoading(true)
    setRenderResult(null)
    try {
      const res = await fetch('/api/scenes/split-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      })
      const data = await res.json()
      setScenes(data.scenes)
      setSelectedSceneIdx(data.scenes.length > 0 ? 0 : null)
    } catch (err) {
      alert('シーン分割に失敗しました: ' + err.message)
    }
    setLoading(false)
  }

  // 尺を再計算
  const recalcDuration = async (updatedScenes, speed) => {
    try {
      const res = await fetch('/api/scenes/calc-duration', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenes: updatedScenes, global_speed: speed }),
      })
      const data = await res.json()
      setScenes(data.scenes)
    } catch (err) {
      console.error('尺の再計算に失敗:', err)
    }
  }

  // 隣接シーンを結合
  const handleMerge = async (index) => {
    try {
      const res = await fetch('/api/scenes/merge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenes, merge_indices: [index] }),
      })
      const data = await res.json()
      if (data.error) {
        alert(data.error)
      } else {
        await recalcDuration(data.scenes, globalSpeed)
      }
    } catch (err) {
      alert('結合に失敗しました: ' + err.message)
    }
  }

  // シーンを分割
  const handleSplit = async (index) => {
    const sceneText = scenes[index].text
    const splitPos = Math.floor(sceneText.length / 2)
    if (splitPos <= 0) return
    try {
      const res = await fetch('/api/scenes/split-scene', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenes, split_index: index, split_position: splitPos }),
      })
      const data = await res.json()
      if (data.error) {
        alert(data.error)
      } else {
        await recalcDuration(data.scenes, globalSpeed)
      }
    } catch (err) {
      alert('分割に失敗しました: ' + err.message)
    }
  }

  // シーンの尺を手動調整
  const handleDurationChange = (index, value) => {
    setScenes(scenes.map((s, i) =>
      i === index ? { ...s, duration: value, manual_duration: value } : s
    ))
  }

  // 手動調整をリセット
  const handleDurationReset = async (index) => {
    const newScenes = scenes.map((s, i) =>
      i === index ? { ...s, manual_duration: null } : s
    )
    await recalcDuration(newScenes, globalSpeed)
  }

  // 全体速度の変更
  const handleGlobalSpeedChange = async (speed) => {
    setGlobalSpeed(speed)
    if (scenes.length > 0) {
      await recalcDuration(scenes, speed)
    }
  }

  // シーンに背景を設定
  const handleBackgroundSelect = (asset) => {
    if (selectedSceneIdx === null) return
    setScenes(scenes.map((s, i) =>
      i === selectedSceneIdx ? { ...s, background: asset ? asset.path : null } : s
    ))
  }

  // Ken Burns ON/OFF切替
  const toggleSceneKenBurns = (index) => {
    setScenes(scenes.map((s, i) =>
      i === index ? { ...s, ken_burns: !s.ken_burns } : s
    ))
  }

  // シーンのTTS ON/OFF切替
  const toggleSceneTts = (index) => {
    setScenes(scenes.map((s, i) =>
      i === index ? { ...s, tts_enabled: !s.tts_enabled } : s
    ))
  }

  // 全シーンのTTS一括ON/OFF
  const toggleAllTts = (enabled) => {
    setScenes(scenes.map((s) => ({ ...s, tts_enabled: enabled })))
  }

  // TTS音声を一括生成
  const handleTtsBatch = async () => {
    if (!ttsAvailable || scenes.length === 0) return
    setTtsGenerating(true)
    try {
      const res = await fetch('/api/tts/batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scenes,
          speaker_id: ttsSpeakerId,
          speed: ttsSpeed,
        }),
      })
      const data = await res.json()
      if (data.success) {
        setScenes(data.scenes)
      } else {
        alert('TTS生成に失敗: ' + (data.error || ''))
      }
    } catch (err) {
      alert('TTS生成に失敗: ' + err.message)
    }
    setTtsGenerating(false)
  }

  // 動画書き出し
  const handleRender = async () => {
    if (scenes.length === 0) return
    setRendering(true)
    setRenderResult(null)
    try {
      const res = await fetch('/api/render/full', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scenes,
          bgm: bgm ? { path: bgm.path } : null,
          bgm_volume: bgmVolume,
          aspect_ratio: aspectRatio,
          transition,
        }),
      })
      const data = await res.json()
      setRenderResult(data)
      if (!data.success) {
        alert('書き出しに失敗しました: ' + (data.error || '不明なエラー'))
      }
    } catch (err) {
      alert('書き出しに失敗しました: ' + err.message)
    }
    setRendering(false)
  }

  // テンプレートを保存
  const handleSaveTemplate = async () => {
    if (!templateName.trim()) return
    try {
      await fetch('/api/templates', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: templateName,
          telop_style: scenes[0]?.telop_style || 'standard',
          transition,
          aspect_ratio: aspectRatio,
          bgm: bgm ? { path: bgm.path } : null,
          bgm_volume: bgmVolume,
          tts_speaker_id: ttsSpeakerId,
          tts_speed: ttsSpeed,
        }),
      })
      loadTemplates()
      setShowTemplateSave(false)
      setTemplateName('')
    } catch (err) {
      alert('テンプレート保存に失敗: ' + err.message)
    }
  }

  // テンプレートを読み込み
  const handleLoadTemplate = async (filename) => {
    try {
      const res = await fetch(`/api/templates/${filename}`)
      const data = await res.json()
      if (data.error) { alert(data.error); return }
      setTransition(data.transition || 'cut')
      setAspectRatio(data.aspect_ratio || '9:16')
      setBgmVolume(data.bgm_volume || 80)
      setTtsSpeakerId(data.tts_speaker_id || 1)
      setTtsSpeed(data.tts_speed || 1.0)
      if (data.telop_style && scenes.length > 0) {
        setScenes(scenes.map((s) => ({ ...s, telop_style: data.telop_style })))
      }
    } catch (err) {
      alert('テンプレート読み込みに失敗: ' + err.message)
    }
  }

  // テンプレートを削除
  const handleDeleteTemplate = async (filename) => {
    try {
      await fetch(`/api/templates/${filename}`, { method: 'DELETE' })
      loadTemplates()
    } catch (err) {
      alert('テンプレート削除に失敗: ' + err.message)
    }
  }

  // プロジェクトを保存
  const handleSaveProject = async () => {
    try {
      const res = await fetch('/api/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: projectName,
          filename: currentProjectFile,
          scenes,
          text,
          bgm: bgm ? { path: bgm.path } : null,
          bgm_volume: bgmVolume,
          transition,
          aspect_ratio: aspectRatio,
          tts_speaker_id: ttsSpeakerId,
          tts_speed: ttsSpeed,
          global_speed: globalSpeed,
        }),
      })
      const data = await res.json()
      if (data.filename) setCurrentProjectFile(data.filename)
      loadProjects()
    } catch (err) {
      alert('プロジェクト保存に失敗: ' + err.message)
    }
  }

  // プロジェクトを読み込み
  const handleLoadProject = async (filename) => {
    try {
      const res = await fetch(`/api/projects/${filename}`)
      const data = await res.json()
      if (data.error) { alert(data.error); return }
      setCurrentProjectFile(filename)
      setProjectName(data.name || 'unnamed')
      setScenes(data.scenes || [])
      setText(data.text || '')
      setTransition(data.transition || 'cut')
      setAspectRatio(data.aspect_ratio || '9:16')
      setBgmVolume(data.bgm_volume || 80)
      setGlobalSpeed(data.global_speed || 1.0)
      setTtsSpeakerId(data.tts_speaker_id || 1)
      setTtsSpeed(data.tts_speed || 1.0)
      setSelectedSceneIdx(data.scenes?.length > 0 ? 0 : null)
      setRenderResult(null)
      setShowProjectList(false)
    } catch (err) {
      alert('プロジェクト読み込みに失敗: ' + err.message)
    }
  }

  // プロジェクトを複製
  const handleDuplicateProject = async (filename) => {
    try {
      await fetch(`/api/projects/${filename}/duplicate`, { method: 'POST' })
      loadProjects()
    } catch (err) {
      alert('プロジェクト複製に失敗: ' + err.message)
    }
  }

  // プロジェクトを削除
  const handleDeleteProject = async (filename) => {
    try {
      await fetch(`/api/projects/${filename}`, { method: 'DELETE' })
      loadProjects()
      if (currentProjectFile === filename) {
        setCurrentProjectFile(null)
        setProjectName('新規プロジェクト')
      }
    } catch (err) {
      alert('プロジェクト削除に失敗: ' + err.message)
    }
  }

  // 新規プロジェクト
  const handleNewProject = () => {
    setCurrentProjectFile(null)
    setProjectName('新規プロジェクト')
    setScenes([])
    setText('')
    setRenderResult(null)
    setSelectedSceneIdx(null)
    setShowProjectList(false)
  }

  // 合計尺
  const totalDuration = scenes.reduce((sum, s) => sum + (s.duration || 0), 0)

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-left">
          <h1>ショート動画ジェネレーター</h1>

          {/* プロジェクト操作 */}
          <button className="btn-small" onClick={() => setShowProjectList(true)}>
            プロジェクト一覧
          </button>
          <button className="btn-small" onClick={handleNewProject}>新規</button>
          <button className="btn-small" onClick={handleSaveProject}>保存</button>

          {/* テンプレート */}
          <div className="template-dropdown">
            <select
              className="select-input"
              value=""
              onChange={(e) => { if (e.target.value) handleLoadTemplate(e.target.value) }}
            >
              <option value="">テンプレート</option>
              {templates.map((t) => (
                <option key={t.filename} value={t.filename}>{t.name}</option>
              ))}
            </select>
          </div>
          <button className="btn-small" onClick={() => setShowTemplateSave(true)}>
            テンプレ保存
          </button>
        </div>
        <div className="header-actions">
          {scenes.length > 0 && (
            <>
              <span className="total-duration">合計: {totalDuration.toFixed(1)}秒</span>
              <button className="btn-preview" onClick={() => setShowPreview(true)}>
                プレビュー
              </button>
              <button className="btn-render" onClick={handleRender} disabled={rendering}>
                {rendering ? '書き出し中...' : '書き出し'}
              </button>
            </>
          )}
        </div>
      </header>

      <main className="app-main">
        <div className="layout">
          {/* 左パネル */}
          <div className="left-panel">
            <section className="text-input-section">
              <h2>テキスト入力</h2>
              <textarea value={text} onChange={(e) => setText(e.target.value)}
                placeholder={'広告文を入力してください\n（改行・句読点でシーンが自動分割されます）'} rows={6} />
              <button className="btn-primary" onClick={handleSplitText}
                disabled={loading || !text.trim()}>
                {loading ? '分割中...' : 'シーンに分割'}
              </button>
            </section>

            {scenes.length > 0 && (
              <section className="speed-section">
                <h2>全体速度: {globalSpeed.toFixed(1)}x</h2>
                <input type="range" min="0.5" max="2.0" step="0.1" value={globalSpeed}
                  onChange={(e) => handleGlobalSpeedChange(parseFloat(e.target.value))}
                  className="speed-slider" />
                <div className="speed-labels"><span>0.5x</span><span>1.0x</span><span>2.0x</span></div>
              </section>
            )}

            {scenes.length > 0 && (
              <section className="scene-list-section">
                <h2>シーン一覧（{scenes.length}シーン）</h2>
                <div className="scene-list">
                  {scenes.map((scene, idx) => (
                    <div key={scene.id}
                      className={`scene-card ${selectedSceneIdx === idx ? 'active' : ''}`}
                      onClick={() => setSelectedSceneIdx(idx)}>
                      <div className="scene-header">
                        <span className="scene-number">シーン {idx + 1}</span>
                        <div className="scene-badges">
                          <button
                            className={`badge ${scene.tts_enabled ? 'badge-on' : 'badge-off'}`}
                            onClick={(e) => { e.stopPropagation(); toggleSceneTts(idx) }}
                            title="TTS ON/OFF切替">
                            TTS:{scene.tts_enabled ? 'ON' : 'OFF'}
                          </button>
                          <button
                            className={`badge ${scene.ken_burns ? 'badge-on' : 'badge-off'}`}
                            onClick={(e) => { e.stopPropagation(); toggleSceneKenBurns(idx) }}
                            title="Ken Burns効果 ON/OFF">
                            KB:{scene.ken_burns ? 'ON' : 'OFF'}
                          </button>
                          <span className="scene-duration">{scene.duration?.toFixed(1)}秒</span>
                        </div>
                      </div>
                      <p className="scene-text">{scene.text}</p>
                      {scene.background && (
                        <div className="scene-bg-preview"><img src={scene.background} alt="背景" /></div>
                      )}
                      <div className="duration-control">
                        <input type="range" min="0.5" max="15.0" step="0.1"
                          value={scene.duration || 1.5}
                          onChange={(e) => handleDurationChange(idx, parseFloat(e.target.value))}
                          className="duration-slider" />
                        <input type="number" min="0.5" max="30" step="0.1"
                          value={scene.duration || 1.5}
                          onChange={(e) => handleDurationChange(idx, parseFloat(e.target.value))}
                          className="duration-input" />
                        <span className="duration-unit">秒</span>
                        {scene.manual_duration != null && (
                          <button className="btn-tiny"
                            onClick={(e) => { e.stopPropagation(); handleDurationReset(idx) }}>自動</button>
                        )}
                      </div>
                      <div className="scene-actions">
                        <select
                          className="select-input select-small"
                          value={scene.telop_style || 'standard'}
                          onChange={(e) => {
                            e.stopPropagation()
                            setScenes(scenes.map((s, i) =>
                              i === idx ? { ...s, telop_style: e.target.value } : s
                            ))
                          }}
                          onClick={(e) => e.stopPropagation()}
                        >
                          <option value="standard">標準</option>
                          <option value="impact">インパクト</option>
                          <option value="subtitle">字幕</option>
                          <option value="pop">ポップ</option>
                        </select>
                        <button className="btn-small" onClick={(e) => { e.stopPropagation(); handleSplit(idx) }}>分割</button>
                        {idx < scenes.length - 1 && (
                          <button className="btn-small" onClick={(e) => { e.stopPropagation(); handleMerge(idx) }}>次と結合</button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
                <div className="total-bar">合計: {totalDuration.toFixed(1)}秒</div>
              </section>
            )}
          </div>

          {/* 中央パネル */}
          <div className="center-panel">
            {renderResult?.success ? (
              <div className="render-result">
                <h3>書き出し完了</h3>
                <video src={renderResult.url} controls className="result-video" />
                <p className="result-info">{renderResult.filename} ({renderResult.duration?.toFixed(1)}秒)</p>
              </div>
            ) : (
              <div className="preview-placeholder">
                {selectedSceneIdx !== null && scenes[selectedSceneIdx]?.background ? (
                  <img src={scenes[selectedSceneIdx].background} alt="プレビュー" className="preview-bg" />
                ) : (
                  <p>プレビューエリア</p>
                )}
                {selectedSceneIdx !== null && scenes[selectedSceneIdx] && (
                  <div className="preview-telop">{scenes[selectedSceneIdx].text}</div>
                )}
              </div>
            )}
          </div>

          {/* 右パネル */}
          <div className="right-panel">
            {scenes.length > 0 && (
              <>
                <div className="panel-section">
                  <AssetPicker assetType="backgrounds" onSelect={handleBackgroundSelect}
                    selectedPath={selectedSceneIdx !== null ? scenes[selectedSceneIdx]?.background : null} />
                </div>

                <div className="panel-section">
                  <AssetPicker assetType="bgm" onSelect={(asset) => setBgm(asset)} selectedPath={bgm?.path} />
                  {bgm && (
                    <div className="bgm-volume">
                      <label>BGM音量: {bgmVolume}%</label>
                      <input type="range" min="0" max="100" value={bgmVolume}
                        onChange={(e) => setBgmVolume(parseInt(e.target.value))} />
                    </div>
                  )}
                </div>

                {/* TTS設定 */}
                <div className="panel-section">
                  <h3 className="section-title">
                    TTS（読み上げ）
                    <span className={`tts-status ${ttsAvailable ? 'on' : 'off'}`}>
                      {ttsAvailable ? '接続OK' : '未接続'}
                    </span>
                  </h3>

                  <div className="tts-controls">
                    <div className="setting-row">
                      <div className="tts-toggle-row">
                        <button className="btn-small" onClick={() => toggleAllTts(true)}>全ON</button>
                        <button className="btn-small" onClick={() => toggleAllTts(false)}>全OFF</button>
                      </div>
                    </div>

                    {ttsAvailable && ttsSpeakers.length > 0 && (
                      <div className="setting-row">
                        <label>話者</label>
                        <select value={ttsSpeakerId} onChange={(e) => setTtsSpeakerId(parseInt(e.target.value))}
                          className="select-input">
                          {ttsSpeakers.map((s) => (
                            <option key={s.id} value={s.id}>{s.name}</option>
                          ))}
                        </select>
                      </div>
                    )}

                    <div className="setting-row">
                      <label>TTS速度: {ttsSpeed.toFixed(1)}x</label>
                      <input type="range" min="0.5" max="2.0" step="0.1" value={ttsSpeed}
                        onChange={(e) => setTtsSpeed(parseFloat(e.target.value))}
                        className="speed-slider" />
                    </div>

                    {ttsAvailable && (
                      <button className="btn-primary" onClick={handleTtsBatch}
                        disabled={ttsGenerating}>
                        {ttsGenerating ? 'TTS生成中...' : 'TTS音声を生成（尺を再計算）'}
                      </button>
                    )}

                    {!ttsAvailable && (
                      <p className="tts-hint">
                        VOICEVOXを起動してからリロードしてください。
                        TTS OFFの場合は文字数から尺を自動算出します。
                      </p>
                    )}
                  </div>
                </div>

                {/* 出力設定 */}
                <div className="panel-section">
                  <h3 className="section-title">出力設定</h3>
                  <div className="setting-row">
                    <label>トランジション</label>
                    <select value={transition} onChange={(e) => setTransition(e.target.value)}
                      className="select-input">
                      <option value="cut">カット（なし）</option>
                      <option value="crossfade">クロスフェード</option>
                      <option value="slide">スライド</option>
                      <option value="wipe">ワイプ</option>
                    </select>
                  </div>
                  <div className="setting-row">
                    <label>アスペクト比</label>
                    <select value={aspectRatio} onChange={(e) => setAspectRatio(e.target.value)}
                      className="select-input">
                      <option value="9:16">9:16（縦長）</option>
                      <option value="1:1">1:1（正方形）</option>
                      <option value="16:9">16:9（横長）</option>
                    </select>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </main>

      {/* プロジェクト一覧ダイアログ */}
      {showProjectList && (
        <div className="modal-overlay" onClick={() => setShowProjectList(false)}>
          <div className="modal modal-wide" onClick={(e) => e.stopPropagation()}>
            <h3>プロジェクト一覧</h3>
            {projects.length === 0 ? (
              <p className="tts-hint">保存済みプロジェクトはありません</p>
            ) : (
              <div className="project-list">
                {projects.map((p) => (
                  <div key={p.filename} className="project-item">
                    <div className="project-info">
                      <strong>{p.name}</strong>
                      <span className="project-meta">
                        {p.scene_count}シーン / {p.total_duration?.toFixed(1)}秒
                      </span>
                    </div>
                    <div className="project-actions">
                      <button className="btn-small" onClick={() => handleLoadProject(p.filename)}>開く</button>
                      <button className="btn-small" onClick={() => handleDuplicateProject(p.filename)}>複製</button>
                      <button className="btn-tiny" onClick={() => handleDeleteProject(p.filename)}>削除</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
            <div className="modal-actions" style={{ marginTop: 12 }}>
              <button className="btn-small" onClick={() => setShowProjectList(false)}>閉じる</button>
            </div>
          </div>
        </div>
      )}

      {/* テンプレート保存ダイアログ */}
      {showTemplateSave && (
        <div className="modal-overlay" onClick={() => setShowTemplateSave(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>テンプレートを保存</h3>
            <input
              type="text"
              placeholder="テンプレート名"
              value={templateName}
              onChange={(e) => setTemplateName(e.target.value)}
              className="modal-input"
              autoFocus
            />
            <div className="modal-actions">
              <button className="btn-primary" onClick={handleSaveTemplate}
                disabled={!templateName.trim()}>保存</button>
              <button className="btn-small" onClick={() => setShowTemplateSave(false)}>キャンセル</button>
            </div>
            {templates.length > 0 && (
              <div className="template-list">
                <h4>既存テンプレート</h4>
                {templates.map((t) => (
                  <div key={t.filename} className="template-item">
                    <span>{t.name}</span>
                    <button className="btn-tiny" onClick={() => handleDeleteTemplate(t.filename)}>
                      削除
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* プレビューオーバーレイ */}
      {showPreview && scenes.length > 0 && (
        <Preview scenes={scenes} onClose={() => setShowPreview(false)} />
      )}
    </div>
  )
}

export default App
