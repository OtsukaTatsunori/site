import { useState, useEffect, useCallback } from 'react'
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
  const [outputFormat, setOutputFormat] = useState('mp4')
  const [rendering, setRendering] = useState(false)
  const [renderResult, setRenderResult] = useState(null)
  const [ttsAvailable, setTtsAvailable] = useState(false)
  const [ttsSpeakers, setTtsSpeakers] = useState([])
  const [ttsSpeakerId, setTtsSpeakerId] = useState(1)
  const [ttsSpeed, setTtsSpeed] = useState(1.0)
  const [ttsGenerating, setTtsGenerating] = useState(false)
  const [showPreview, setShowPreview] = useState(false)
  const [templates, setTemplates] = useState([])
  const [showTemplateSave, setShowTemplateSave] = useState(false)
  const [templateName, setTemplateName] = useState('')
  const [projects, setProjects] = useState([])
  const [currentProjectFile, setCurrentProjectFile] = useState(null)
  const [projectName, setProjectName] = useState('')
  const [showProjectList, setShowProjectList] = useState(false)
  const [telopPresets, setTelopPresets] = useState([])
  const [fonts, setFonts] = useState([])

  // Undo/Redo
  const [history, setHistory] = useState([])
  const [historyIdx, setHistoryIdx] = useState(-1)

  const pushHistory = useCallback((newScenes) => {
    const newHistory = history.slice(0, historyIdx + 1)
    newHistory.push(JSON.stringify(newScenes))
    if (newHistory.length > 50) newHistory.shift()
    setHistory(newHistory)
    setHistoryIdx(newHistory.length - 1)
  }, [history, historyIdx])

  const undo = () => {
    if (historyIdx > 0) {
      const prev = historyIdx - 1
      setHistoryIdx(prev)
      setScenes(JSON.parse(history[prev]))
    }
  }
  const redo = () => {
    if (historyIdx < history.length - 1) {
      const next = historyIdx + 1
      setHistoryIdx(next)
      setScenes(JSON.parse(history[next]))
    }
  }

  const updateScenes = (newScenes) => {
    setScenes(newScenes)
    pushHistory(newScenes)
  }

  const loadTemplates = () => {
    fetch('/api/templates').then(r => r.json()).then(d => setTemplates(d.templates || []))
  }
  const loadProjects = () => {
    fetch('/api/projects').then(r => r.json()).then(d => setProjects(d.projects || []))
  }

  useEffect(() => {
    loadTemplates()
    loadProjects()
    fetch('/api/telop-presets').then(r => r.json()).then(d => setTelopPresets(d.presets || []))
    fetch('/api/assets/fonts').then(r => r.json()).then(d => setFonts(d.assets || []))
    fetch('/api/tts/status').then(r => r.json()).then(d => {
      setTtsAvailable(d.available)
      if (d.available) fetch('/api/tts/speakers').then(r => r.json()).then(d2 => setTtsSpeakers(d2.speakers || []))
    }).catch(() => setTtsAvailable(false))
  }, [])

  // キーボードショートカット
  useEffect(() => {
    const handler = (e) => {
      const tag = (e.target.tagName || '').toLowerCase()
      const isTyping = tag === 'input' || tag === 'textarea' || e.target.isContentEditable
      const mod = e.ctrlKey || e.metaKey
      if (mod && e.key === 'z' && !e.shiftKey) { e.preventDefault(); undo(); return }
      if (mod && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) { e.preventDefault(); redo(); return }
      if (mod && e.key === 's') { e.preventDefault(); handleSaveProject(); return }
      if (!isTyping) {
        if (e.key === 'ArrowLeft' && selectedSceneIdx !== null && selectedSceneIdx > 0) {
          e.preventDefault(); setSelectedSceneIdx(selectedSceneIdx - 1)
        } else if (e.key === 'ArrowRight' && selectedSceneIdx !== null && selectedSceneIdx < scenes.length - 1) {
          e.preventDefault(); setSelectedSceneIdx(selectedSceneIdx + 1)
        }
      }
    }
    window.addEventListener('keydown', handler)
    return () => window.removeEventListener('keydown', handler)
  }, [history, historyIdx, scenes, selectedSceneIdx, projectName, currentProjectFile])

  const handleSplitText = async () => {
    if (!text.trim()) return
    setLoading(true)
    setRenderResult(null)
    try {
      const res = await fetch('/api/scenes/split-text', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      })
      const data = await res.json()
      updateScenes(data.scenes)
      setSelectedSceneIdx(data.scenes.length > 0 ? 0 : null)
    } catch (err) { alert('Error: ' + err.message) }
    setLoading(false)
  }

  const recalcDuration = async (s, speed) => {
    try {
      const res = await fetch('/api/scenes/calc-duration', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenes: s, global_speed: speed }),
      })
      const data = await res.json()
      updateScenes(data.scenes)
    } catch (err) { console.error(err) }
  }

  const handleMerge = async (index) => {
    const res = await fetch('/api/scenes/merge', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenes, merge_indices: [index] }),
    })
    const data = await res.json()
    if (!data.error) await recalcDuration(data.scenes, globalSpeed)
  }

  const handleSplit = async (index) => {
    const splitPos = Math.floor(scenes[index].text.length / 2)
    if (splitPos <= 0) return
    const res = await fetch('/api/scenes/split-scene', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenes, split_index: index, split_position: splitPos }),
    })
    const data = await res.json()
    if (!data.error) await recalcDuration(data.scenes, globalSpeed)
  }

  const handleDurationChange = (index, value) => {
    updateScenes(scenes.map((s, i) => i === index ? { ...s, duration: value, manual_duration: value } : s))
  }

  const handleDurationReset = async (index) => {
    await recalcDuration(scenes.map((s, i) => i === index ? { ...s, manual_duration: null } : s), globalSpeed)
  }

  const handleGlobalSpeedChange = async (speed) => {
    setGlobalSpeed(speed)
    if (scenes.length > 0) await recalcDuration(scenes, speed)
  }

  const handleBackgroundSelect = (asset) => {
    if (selectedSceneIdx === null) return
    updateScenes(scenes.map((s, i) => i === selectedSceneIdx ? { ...s, background: asset ? asset.path : null } : s))
  }

  const handleOverlaySelect = (asset) => {
    if (selectedSceneIdx === null) return
    updateScenes(scenes.map((s, i) => i === selectedSceneIdx ? { ...s, overlay_image: asset ? asset.path : null } : s))
  }

  const toggleSceneKenBurns = (idx) => updateScenes(scenes.map((s, i) => i === idx ? { ...s, ken_burns: !s.ken_burns } : s))
  const toggleSceneTts = (idx) => updateScenes(scenes.map((s, i) => i === idx ? { ...s, tts_enabled: !s.tts_enabled } : s))
  const toggleAllTts = (on) => updateScenes(scenes.map(s => ({ ...s, tts_enabled: on })))

  const handleTtsBatch = async () => {
    if (!ttsAvailable || !scenes.length) return
    setTtsGenerating(true)
    try {
      const res = await fetch('/api/tts/batch', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenes, speaker_id: ttsSpeakerId, speed: ttsSpeed }),
      })
      const data = await res.json()
      if (data.success) updateScenes(data.scenes)
      else alert('TTS error: ' + (data.error || ''))
    } catch (err) { alert(err.message) }
    setTtsGenerating(false)
  }

  const handleRender = async (quick = false) => {
    if (!scenes.length) return
    setRendering(true); setRenderResult(null)
    try {
      const endpoint = quick ? '/api/render/preview' : '/api/render/full'
      const res = await fetch(endpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenes, bgm: bgm ? { path: bgm.path, offset: bgm.offset || 0 } : null, bgm_volume: bgmVolume, aspect_ratio: aspectRatio, transition, output_format: outputFormat }),
      })
      const data = await res.json()
      setRenderResult(data)
      if (!data.success) alert('Error: ' + (data.error || ''))
    } catch (err) { alert(err.message) }
    setRendering(false)
  }

  const handleSaveTemplate = async () => {
    if (!templateName.trim()) return
    await fetch('/api/templates', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: templateName, telop_style: scenes[0]?.telop_style || 'standard', transition, aspect_ratio: aspectRatio, bgm: bgm ? { path: bgm.path, offset: bgm.offset || 0 } : null, bgm_volume: bgmVolume, tts_speaker_id: ttsSpeakerId, tts_speed: ttsSpeed }),
    })
    loadTemplates(); setShowTemplateSave(false); setTemplateName('')
  }

  const handleLoadTemplate = async (fn) => {
    const data = await (await fetch(`/api/templates/${fn}`)).json()
    if (data.error) return
    setTransition(data.transition || 'cut'); setAspectRatio(data.aspect_ratio || '9:16')
    setBgmVolume(data.bgm_volume || 80); setTtsSpeakerId(data.tts_speaker_id || 1); setTtsSpeed(data.tts_speed || 1.0)
    if (data.telop_style && scenes.length) updateScenes(scenes.map(s => ({ ...s, telop_style: data.telop_style })))
  }

  const handleDeleteTemplate = async (fn) => { await fetch(`/api/templates/${fn}`, { method: 'DELETE' }); loadTemplates() }

  const handleSaveProject = async () => {
    const res = await fetch('/api/projects', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: projectName, filename: currentProjectFile, scenes, text, bgm: bgm ? { path: bgm.path, offset: bgm.offset || 0 } : null, bgm_volume: bgmVolume, transition, aspect_ratio: aspectRatio, tts_speaker_id: ttsSpeakerId, tts_speed: ttsSpeed, global_speed: globalSpeed }),
    })
    const data = await res.json()
    if (data.filename) setCurrentProjectFile(data.filename)
    loadProjects()
  }

  const handleLoadProject = async (fn) => {
    const data = await (await fetch(`/api/projects/${fn}`)).json()
    if (data.error) return
    setCurrentProjectFile(fn); setProjectName(data.name || ''); setScenes(data.scenes || []); setText(data.text || '')
    setTransition(data.transition || 'cut'); setAspectRatio(data.aspect_ratio || '9:16'); setBgmVolume(data.bgm_volume || 80)
    setGlobalSpeed(data.global_speed || 1.0); setTtsSpeakerId(data.tts_speaker_id || 1); setTtsSpeed(data.tts_speed || 1.0)
    setSelectedSceneIdx(data.scenes?.length > 0 ? 0 : null); setRenderResult(null); setShowProjectList(false)
  }

  const handleDuplicateProject = async (fn) => { await fetch(`/api/projects/${fn}/duplicate`, { method: 'POST' }); loadProjects() }
  const handleDeleteProject = async (fn) => {
    await fetch(`/api/projects/${fn}`, { method: 'DELETE' }); loadProjects()
    if (currentProjectFile === fn) { setCurrentProjectFile(null); setProjectName('') }
  }
  const handleNewProject = () => { setCurrentProjectFile(null); setProjectName(''); setScenes([]); setText(''); setRenderResult(null); setSelectedSceneIdx(null); setShowProjectList(false) }

  // telop position change
  const setTelopPos = (idx, field, val) => {
    updateScenes(scenes.map((s, i) => i === idx ? { ...s, [field]: parseInt(val) || null } : s))
  }

  // custom box
  const setCustomBox = (idx, boxProps) => {
    const cur = scenes[idx].custom_box || { enabled: false, color: '#000000', opacity: 0.6, padding: 10 }
    updateScenes(scenes.map((s, i) => i === idx ? { ...s, custom_box: { ...cur, ...boxProps } } : s))
  }

  // scene field update (generic)
  const updateSceneField = (idx, field, val) => {
    updateScenes(scenes.map((s, i) => i === idx ? { ...s, [field]: val } : s))
  }

  // シーン複製
  const duplicateScene = (idx) => {
    const source = scenes[idx]
    const maxId = scenes.reduce((m, s) => Math.max(m, s.id || 0), 0)
    const copy = { ...source, id: maxId + 1, tts_path: undefined }
    const newScenes = [...scenes.slice(0, idx + 1), copy, ...scenes.slice(idx + 1)]
    updateScenes(newScenes)
  }

  // シーン削除
  const deleteScene = (idx) => {
    const newScenes = scenes.filter((_, i) => i !== idx)
    updateScenes(newScenes)
    if (selectedSceneIdx === idx) setSelectedSceneIdx(newScenes.length > 0 ? Math.min(idx, newScenes.length - 1) : null)
  }

  // D&D 並び替え
  const [dragIdx, setDragIdx] = useState(null)
  const [dragOverIdx, setDragOverIdx] = useState(null)
  const handleDragStart = (idx) => setDragIdx(idx)
  const handleDragOver = (e, idx) => { e.preventDefault(); if (idx !== dragOverIdx) setDragOverIdx(idx) }
  const handleDrop = (e, idx) => {
    e.preventDefault()
    if (dragIdx === null || dragIdx === idx) { setDragIdx(null); setDragOverIdx(null); return }
    const newScenes = [...scenes]
    const [moved] = newScenes.splice(dragIdx, 1)
    newScenes.splice(idx, 0, moved)
    updateScenes(newScenes)
    setDragIdx(null); setDragOverIdx(null)
    setSelectedSceneIdx(idx)
  }
  const handleDragEnd = () => { setDragIdx(null); setDragOverIdx(null) }

  // apply fields to all scenes (一括適用)
  const applyToAll = (fields) => {
    updateScenes(scenes.map(s => ({ ...s, ...fields })))
  }

  const sel = selectedSceneIdx !== null ? scenes[selectedSceneIdx] : null
  const totalDuration = scenes.reduce((sum, s) => sum + (s.duration || 0), 0)

  // プレビューのスタイル計算 (9:16 = 270 x 480 の比率)
  const PREVIEW_W = 270
  const PREVIEW_H = 480
  // 元の解像度は 1080x1920 → スケール
  const SCALE = PREVIEW_W / 1080

  const getPresetStyle = (scene) => {
    const p = telopPresets.find(t => t.id === scene?.telop_style) || {}
    const fontsize = scene?.telop_fontsize || p.fontsize || 56
    return {
      fontSize: `${fontsize * SCALE}px`,
      color: p.fontcolor || 'white',
      WebkitTextStroke: `${(p.borderw || 2) * SCALE}px ${p.bordercolor || 'black'}`,
      textAlign: 'center',
      lineHeight: 1.2,
      fontWeight: 'bold',
      fontFamily: scene?.telop_font ? 'system-ui' : 'inherit',
      whiteSpace: 'pre-wrap',
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-left">
          <h1>Short Video Gen</h1>
          <button className="btn-small" onClick={() => setShowProjectList(true)}>PJ</button>
          <button className="btn-small" onClick={handleNewProject}>New</button>
          <button className="btn-small" onClick={handleSaveProject}>Save</button>
          <div className="template-dropdown">
            <select className="select-input" value="" onChange={e => { if (e.target.value) handleLoadTemplate(e.target.value) }}>
              <option value="">Template</option>
              {templates.map(t => <option key={t.filename} value={t.filename}>{t.name}</option>)}
            </select>
          </div>
          <button className="btn-small" onClick={() => setShowTemplateSave(true)}>T+</button>
          <button className="btn-small" onClick={undo} disabled={historyIdx <= 0} title="Undo">&#9664;</button>
          <button className="btn-small" onClick={redo} disabled={historyIdx >= history.length - 1} title="Redo">&#9654;</button>
        </div>
        <div className="header-actions">
          {scenes.length > 0 && (
            <>
              <span className="total-duration">{totalDuration.toFixed(1)}s</span>
              <button className="btn-preview" onClick={() => setShowPreview(true)}>Preview</button>
              <button className="btn-small" onClick={() => handleRender(true)} disabled={rendering} title="低解像度クイックプレビュー">
                {rendering ? '...' : 'Quick'}
              </button>
              <button className="btn-render" onClick={() => handleRender(false)} disabled={rendering}>
                {rendering ? 'Rendering...' : 'Export'}
              </button>
            </>
          )}
        </div>
      </header>

      <main className="app-main">
        <div className="layout">
          {/* Left panel */}
          <div className="left-panel">
            <section className="text-input-section">
              <h2>Text Input</h2>
              <textarea value={text} onChange={e => setText(e.target.value)}
                placeholder={'Enter ad text here\n(Split by line breaks / punctuation)'} rows={6} />
              <button className="btn-primary" onClick={handleSplitText} disabled={loading || !text.trim()}>
                {loading ? '...' : 'Split into Scenes'}
              </button>
            </section>

            {scenes.length > 0 && (
              <section className="speed-section">
                <h2>Speed: {globalSpeed.toFixed(1)}x</h2>
                <input type="range" min="0.5" max="5.0" step="0.1" value={globalSpeed}
                  onChange={e => handleGlobalSpeedChange(parseFloat(e.target.value))} className="speed-slider" />
                <div className="speed-labels"><span>0.5x</span><span>1.0x</span><span>2.0x</span><span>5.0x</span></div>
              </section>
            )}

            {scenes.length > 0 && (
              <section className="scene-list-section">
                <h2>Scenes ({scenes.length})</h2>
                <div className="scene-list">
                  {scenes.map((scene, idx) => (
                    <div key={scene.id} className={`scene-card ${selectedSceneIdx === idx ? 'active' : ''} ${dragIdx === idx ? 'dragging' : ''} ${dragOverIdx === idx && dragIdx !== idx ? 'drop-target' : ''}`}
                      draggable
                      onDragStart={() => handleDragStart(idx)}
                      onDragOver={e => handleDragOver(e, idx)}
                      onDrop={e => handleDrop(e, idx)}
                      onDragEnd={handleDragEnd}
                      onClick={() => setSelectedSceneIdx(idx)}>
                      <div className="scene-header">
                        <span className="scene-number">#{idx + 1}</span>
                        <div className="scene-badges">
                          <button className={`badge ${scene.tts_enabled ? 'badge-on' : 'badge-off'}`}
                            onClick={e => { e.stopPropagation(); toggleSceneTts(idx) }}>TTS</button>
                          <button className={`badge ${scene.ken_burns ? 'badge-on' : 'badge-off'}`}
                            onClick={e => { e.stopPropagation(); toggleSceneKenBurns(idx) }}>KB</button>
                          <span className="scene-duration">{scene.duration?.toFixed(1)}s</span>
                        </div>
                      </div>
                      <p className="scene-text">{scene.text}</p>
                      {scene.background && <div className="scene-bg-preview"><img src={scene.background} alt="" /></div>}
                      {scene.overlay_image && <div className="scene-overlay-badge">+ overlay</div>}
                      {scene.se_path && <div className="scene-overlay-badge">♪ SE</div>}
                      <div className="duration-control">
                        <input type="range" min="0.5" max="15.0" step="0.1" value={scene.duration || 1.5}
                          onChange={e => handleDurationChange(idx, parseFloat(e.target.value))} className="duration-slider" />
                        <input type="number" min="0.5" max="30" step="0.1" value={scene.duration || 1.5}
                          onChange={e => handleDurationChange(idx, parseFloat(e.target.value))} className="duration-input" />
                        <span className="duration-unit">s</span>
                        {scene.manual_duration != null && (
                          <button className="btn-tiny" onClick={e => { e.stopPropagation(); handleDurationReset(idx) }}>Auto</button>
                        )}
                      </div>
                      <div className="scene-actions">
                        <select className="select-input select-small" value={scene.telop_style || 'standard'}
                          onChange={e => { e.stopPropagation(); updateScenes(scenes.map((s, i) => i === idx ? { ...s, telop_style: e.target.value } : s)) }}
                          onClick={e => e.stopPropagation()}>
                          {telopPresets.map(p => <option key={p.id} value={p.id}>{p.label}</option>)}
                        </select>
                        <select className="select-input select-small" value={scene.text_anim || 'none'}
                          onChange={e => { e.stopPropagation(); updateScenes(scenes.map((s, i) => i === idx ? { ...s, text_anim: e.target.value } : s)) }}
                          onClick={e => e.stopPropagation()} title="テキストアニメーション">
                          <option value="none">アニメ無し</option>
                          <option value="typewriter">タイプライター</option>
                          <option value="popin">ポップイン</option>
                          <option value="slide_in">スライドイン</option>
                        </select>
                        <button className="btn-small" onClick={e => { e.stopPropagation(); handleSplit(idx) }}>Split</button>
                        {idx < scenes.length - 1 && (
                          <button className="btn-small" onClick={e => { e.stopPropagation(); handleMerge(idx) }}>Merge</button>
                        )}
                        <button className="btn-small" onClick={e => { e.stopPropagation(); duplicateScene(idx) }} title="複製">Dup</button>
                        <button className="btn-tiny" onClick={e => { e.stopPropagation(); deleteScene(idx) }} title="削除">×</button>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="total-bar">Total: {totalDuration.toFixed(1)}s</div>
              </section>
            )}
          </div>

          {/* Center panel - Preview */}
          <div className="center-panel">
            {renderResult?.success ? (
              <div className="render-result">
                <h3>Export Complete</h3>
                <video src={renderResult.url} controls className="result-video" />
                <p className="result-info">{renderResult.filename} ({renderResult.duration?.toFixed(1)}s)</p>
              </div>
            ) : (
              <div className="preview-frame">
                <div className="preview-screen-9x16">
                  {sel?.background ? (
                    <img src={sel.background} alt="" className="preview-bg-img" />
                  ) : (
                    <div className="preview-bg-black" />
                  )}
                  {sel?.overlay_image && (
                    <img src={sel.overlay_image} alt="" className="preview-overlay-img"
                      style={{
                        width: `${(sel.overlay_scale ?? 80)}%`,
                        left: sel.overlay_x != null ? `${sel.overlay_x / 10.8}%` : '50%',
                        top: sel.overlay_y != null ? `${sel.overlay_y / 19.2}%` : '50%',
                        transform: sel.overlay_x != null ? 'none' : 'translate(-50%, -50%)',
                      }} />
                  )}
                  {sel && (
                    <div className="preview-telop-inner"
                      style={{
                        ...getPresetStyle(sel),
                        position: 'absolute',
                        left: sel.telop_x != null ? `${sel.telop_x / 10.8}%` : '50%',
                        top: sel.telop_y != null ? `${sel.telop_y / 19.2}%` : 'auto',
                        bottom: sel.telop_y != null ? 'auto' : '12%',
                        transform: sel.telop_x != null ? 'none' : 'translateX(-50%)',
                        maxWidth: '85%',
                        ...(sel.custom_box?.enabled ? {
                          background: sel.custom_box.color + Math.round((sel.custom_box.opacity || 0.6) * 255).toString(16).padStart(2, '0'),
                          borderRadius: (sel.custom_box.radius || 6) + 'px',
                          padding: ((sel.custom_box.padding || 10) * SCALE * 2) + 'px',
                        } : {}),
                      }}>
                      {sel.text}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Right panel */}
          <div className="right-panel">
            {scenes.length > 0 && (
              <>
                <div className="panel-section">
                  <AssetPicker assetType="backgrounds" onSelect={handleBackgroundSelect}
                    selectedPath={sel?.background} />
                </div>

                <div className="panel-section">
                  <AssetPicker assetType="overlays" onSelect={handleOverlaySelect}
                    selectedPath={sel?.overlay_image} label="Overlay Image" />
                </div>

                <div className="panel-section">
                  <AssetPicker assetType="bgm" onSelect={a => setBgm(a)} selectedPath={bgm?.path} />
                  {bgm && (
                    <div className="bgm-volume">
                      <label>BGM Vol: {bgmVolume}%</label>
                      <input type="range" min="0" max="100" value={bgmVolume} onChange={e => setBgmVolume(parseInt(e.target.value))} />
                      <label>BGM Start: {(bgm.offset || 0).toFixed(1)}s</label>
                      <input type="range" min="0" max="60" step="0.5" value={bgm.offset || 0}
                        onChange={e => setBgm({ ...bgm, offset: parseFloat(e.target.value) })} />
                    </div>
                  )}
                </div>

                {sel && (
                  <div className="panel-section">
                    <AssetPicker assetType="se" onSelect={a => updateSceneField(selectedSceneIdx, 'se_path', a ? a.path : null)}
                      selectedPath={sel.se_path} label="効果音 (SE)" />
                    <p className="tts-hint">※ SE は BGM と一緒に書き出し時のみ再生されます</p>
                  </div>
                )}

                {sel && (
                  <div className="panel-section">
                    <h3 className="section-title">映像演出</h3>
                    <div className="setting-row">
                      <label>効果</label>
                      <select className="select-input" value={sel.emphasis_effect || 'none'}
                        onChange={e => updateSceneField(selectedSceneIdx, 'emphasis_effect', e.target.value)}>
                        <option value="none">無し</option>
                        <option value="zoom">ズームイン</option>
                        <option value="shake">シェイク</option>
                      </select>
                    </div>
                    <button className="btn-small btn-apply-all" onClick={() => applyToAll({ emphasis_effect: sel.emphasis_effect })}>全シーンに適用</button>
                  </div>
                )}

                {sel && (
                  <div className="panel-section">
                    <h3 className="section-title">色調補正</h3>
                    {['contrast','brightness','saturation'].map(k => {
                      const range = k === 'brightness' ? [-0.5, 0.5, 0.05] : [0.5, 2.0, 0.05]
                      const def = k === 'brightness' ? 0 : 1
                      const cur = sel.color_adjust?.[k] ?? def
                      return (
                        <div key={k} className="setting-row">
                          <label>{k}: {cur.toFixed(2)}</label>
                          <input type="range" min={range[0]} max={range[1]} step={range[2]} value={cur}
                            onChange={e => {
                              const ca = { ...(sel.color_adjust || {}), [k]: parseFloat(e.target.value) }
                              updateSceneField(selectedSceneIdx, 'color_adjust', ca)
                            }} />
                        </div>
                      )
                    })}
                    <div className="setting-row">
                      <label><input type="checkbox" checked={sel.color_adjust?.vignette || false}
                        onChange={e => {
                          const ca = { ...(sel.color_adjust || {}), vignette: e.target.checked }
                          updateSceneField(selectedSceneIdx, 'color_adjust', ca)
                        }} /> ビネット</label>
                    </div>
                    <div className="btn-row">
                      <button className="btn-small" onClick={() => updateSceneField(selectedSceneIdx, 'color_adjust', null)}>リセット</button>
                      <button className="btn-small btn-apply-all" onClick={() => applyToAll({ color_adjust: sel.color_adjust })}>全シーンに適用</button>
                    </div>
                  </div>
                )}

                {sel && (
                  <div className="panel-section">
                    <h3 className="section-title">強調ワード</h3>
                    <textarea className="emphasis-textarea" value={sel.text || ''}
                      onChange={e => updateSceneField(selectedSceneIdx, 'text', e.target.value)}
                      rows={2} placeholder="本文を範囲選択して「強調に追加」"
                      id={`scene-text-${selectedSceneIdx}`} />
                    <div className="btn-row">
                      {['color','size','box'].map(style => (
                        <button key={style} className="btn-small" onClick={() => {
                          const ta = document.getElementById(`scene-text-${selectedSceneIdx}`)
                          if (!ta) return
                          const sel_text = ta.value.substring(ta.selectionStart, ta.selectionEnd).trim()
                          if (!sel_text) { alert('本文を範囲選択してください'); return }
                          const cur = sel.emphasis_ranges || []
                          updateSceneField(selectedSceneIdx, 'emphasis_ranges', [...cur, { text: sel_text, style }])
                        }}>+ {style === 'color' ? '色' : style === 'size' ? '大' : '枠'}</button>
                      ))}
                    </div>
                    {(sel.emphasis_ranges || []).length > 0 && (
                      <div className="emphasis-list">
                        {sel.emphasis_ranges.map((e, i) => (
                          <div key={i} className={`emphasis-badge emphasis-${e.style}`}>
                            <span>{e.text}</span>
                            <button className="btn-tiny" onClick={() => {
                              const next = sel.emphasis_ranges.filter((_, j) => j !== i)
                              updateSceneField(selectedSceneIdx, 'emphasis_ranges', next)
                            }}>×</button>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* Telop position & size */}
                {sel && (
                  <div className="panel-section">
                    <h3 className="section-title">文字 位置・サイズ・フォント</h3>
                    <div className="setting-row">
                      <label>X: {sel.telop_x ?? 'auto'}</label>
                      <input type="range" min="0" max="1080" step="10" value={sel.telop_x ?? 540}
                        onChange={e => setTelopPos(selectedSceneIdx, 'telop_x', e.target.value)} />
                    </div>
                    <div className="setting-row">
                      <label>Y: {sel.telop_y ?? 'auto'}</label>
                      <input type="range" min="0" max="1920" step="10" value={sel.telop_y ?? 1600}
                        onChange={e => setTelopPos(selectedSceneIdx, 'telop_y', e.target.value)} />
                    </div>
                    <div className="setting-row">
                      <label>サイズ: {sel.telop_fontsize ?? 'auto'}</label>
                      <input type="range" min="20" max="120" step="2"
                        value={sel.telop_fontsize ?? (telopPresets.find(t => t.id === sel.telop_style)?.fontsize || 56)}
                        onChange={e => updateSceneField(selectedSceneIdx, 'telop_fontsize', parseInt(e.target.value))} />
                    </div>
                    {fonts.length > 0 && (
                      <div className="setting-row">
                        <label>フォント</label>
                        <select value={sel.telop_font || ''} onChange={e => updateSceneField(selectedSceneIdx, 'telop_font', e.target.value || null)} className="select-input">
                          <option value="">デフォルト</option>
                          {fonts.map(f => <option key={f.path} value={f.path}>{f.filename}</option>)}
                        </select>
                      </div>
                    )}
                    <div className="btn-row">
                      <button className="btn-small" onClick={() => {
                        updateScenes(scenes.map((s, i) => i === selectedSceneIdx ? { ...s, telop_x: null, telop_y: null, telop_fontsize: null } : s))
                      }}>リセット</button>
                      <button className="btn-small btn-apply-all" onClick={() => applyToAll({
                        telop_x: sel.telop_x, telop_y: sel.telop_y,
                        telop_fontsize: sel.telop_fontsize, telop_font: sel.telop_font,
                      })}>全シーンに適用</button>
                    </div>
                  </div>
                )}

                {/* Overlay position & size */}
                {sel?.overlay_image && (
                  <div className="panel-section">
                    <h3 className="section-title">画像オーバーレイ 位置</h3>
                    <div className="setting-row">
                      <label>X: {sel.overlay_x ?? 'center'}</label>
                      <input type="range" min="0" max="1080" step="10" value={sel.overlay_x ?? 540}
                        onChange={e => updateSceneField(selectedSceneIdx, 'overlay_x', parseInt(e.target.value))} />
                    </div>
                    <div className="setting-row">
                      <label>Y: {sel.overlay_y ?? 'center'}</label>
                      <input type="range" min="0" max="1920" step="10" value={sel.overlay_y ?? 960}
                        onChange={e => updateSceneField(selectedSceneIdx, 'overlay_y', parseInt(e.target.value))} />
                    </div>
                    <div className="setting-row">
                      <label>サイズ: {sel.overlay_scale ?? 80}%</label>
                      <input type="range" min="10" max="100" step="5"
                        value={sel.overlay_scale ?? 80}
                        onChange={e => updateSceneField(selectedSceneIdx, 'overlay_scale', parseInt(e.target.value))} />
                    </div>
                    <div className="btn-row">
                      <button className="btn-small" onClick={() => {
                        updateScenes(scenes.map((s, i) => i === selectedSceneIdx ? { ...s, overlay_x: null, overlay_y: null, overlay_scale: 80 } : s))
                      }}>リセット</button>
                      <button className="btn-small btn-apply-all" onClick={() => applyToAll({
                        overlay_x: sel.overlay_x, overlay_y: sel.overlay_y, overlay_scale: sel.overlay_scale,
                      })}>全シーンに適用</button>
                    </div>
                  </div>
                )}

                {/* Telop style (preset) */}
                {sel && (
                  <div className="panel-section">
                    <h3 className="section-title">文字デザイン（プリセット）</h3>
                    <div className="setting-row">
                      <select className="select-input" value={sel.telop_style || 'standard'}
                        onChange={e => updateSceneField(selectedSceneIdx, 'telop_style', e.target.value)}>
                        {telopPresets.map(p => <option key={p.id} value={p.id}>{p.label}</option>)}
                      </select>
                    </div>
                    <button className="btn-small btn-apply-all" onClick={() => applyToAll({ telop_style: sel.telop_style })}>全シーンに適用</button>
                  </div>
                )}

                {/* Telop background box */}
                {sel && (
                  <div className="panel-section">
                    <h3 className="section-title">文字の背景帯</h3>
                    <div className="setting-row">
                      <label>
                        <input type="checkbox" checked={sel.custom_box?.enabled || false}
                          onChange={e => setCustomBox(selectedSceneIdx, { enabled: e.target.checked })} />
                        {' '}Enable
                      </label>
                    </div>
                    {sel.custom_box?.enabled && (
                      <>
                        <div className="setting-row">
                          <label>Color</label>
                          <input type="color" value={sel.custom_box?.color || '#000000'}
                            onChange={e => setCustomBox(selectedSceneIdx, { color: e.target.value })} />
                        </div>
                        <div className="setting-row">
                          <label>Opacity: {(sel.custom_box?.opacity ?? 0.6).toFixed(1)}</label>
                          <input type="range" min="0" max="1" step="0.1" value={sel.custom_box?.opacity ?? 0.6}
                            onChange={e => setCustomBox(selectedSceneIdx, { opacity: parseFloat(e.target.value) })} />
                        </div>
                        <div className="setting-row">
                          <label>Roundness: {sel.custom_box?.radius ?? 6}px</label>
                          <input type="range" min="0" max="30" step="1" value={sel.custom_box?.radius ?? 6}
                            onChange={e => setCustomBox(selectedSceneIdx, { radius: parseInt(e.target.value) })} />
                        </div>
                        <div className="setting-row">
                          <label>Padding: {sel.custom_box?.padding ?? 10}px</label>
                          <input type="range" min="0" max="30" step="1" value={sel.custom_box?.padding ?? 10}
                            onChange={e => setCustomBox(selectedSceneIdx, { padding: parseInt(e.target.value) })} />
                        </div>
                      </>
                    )}
                    <button className="btn-small btn-apply-all" onClick={() => applyToAll({ custom_box: sel.custom_box })}>全シーンに適用</button>
                  </div>
                )}

                {/* TTS */}
                <div className="panel-section">
                  <h3 className="section-title">TTS <span className={`tts-status ${ttsAvailable ? 'on' : 'off'}`}>{ttsAvailable ? 'OK' : 'OFF'}</span></h3>
                  <div className="tts-controls">
                    <div className="tts-toggle-row">
                      <button className="btn-small" onClick={() => toggleAllTts(true)}>All ON</button>
                      <button className="btn-small" onClick={() => toggleAllTts(false)}>All OFF</button>
                    </div>
                    {ttsAvailable && ttsSpeakers.length > 0 && (
                      <div className="setting-row">
                        <label>Speaker</label>
                        <select value={ttsSpeakerId} onChange={e => setTtsSpeakerId(parseInt(e.target.value))} className="select-input">
                          {ttsSpeakers.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                        </select>
                      </div>
                    )}
                    <div className="setting-row">
                      <label>TTS Speed: {ttsSpeed.toFixed(1)}x</label>
                      <input type="range" min="0.5" max="2.0" step="0.1" value={ttsSpeed} onChange={e => setTtsSpeed(parseFloat(e.target.value))} className="speed-slider" />
                    </div>
                    {ttsAvailable && <button className="btn-primary" onClick={handleTtsBatch} disabled={ttsGenerating}>{ttsGenerating ? '...' : 'Generate TTS'}</button>}
                    {!ttsAvailable && <p className="tts-hint">Start VOICEVOX and reload.</p>}
                  </div>
                </div>

                {/* Output */}
                <div className="panel-section">
                  <h3 className="section-title">Output</h3>
                  <div className="setting-row">
                    <label>Transition</label>
                    <select value={transition} onChange={e => setTransition(e.target.value)} className="select-input">
                      <option value="cut">Cut</option><option value="crossfade">Crossfade</option>
                      <option value="slide">Slide</option><option value="wipe">Wipe</option>
                    </select>
                  </div>
                  <div className="setting-row">
                    <label>Aspect Ratio</label>
                    <select value={aspectRatio} onChange={e => setAspectRatio(e.target.value)} className="select-input">
                      <option value="9:16">9:16</option><option value="1:1">1:1</option><option value="16:9">16:9</option>
                    </select>
                  </div>
                  <div className="setting-row">
                    <label>Format</label>
                    <select value={outputFormat} onChange={e => setOutputFormat(e.target.value)} className="select-input">
                      <option value="mp4">MP4</option>
                      <option value="gif">GIF</option>
                    </select>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </main>

      {showProjectList && (
        <div className="modal-overlay" onClick={() => setShowProjectList(false)}>
          <div className="modal modal-wide" onClick={e => e.stopPropagation()}>
            <h3>Projects</h3>
            {projects.length === 0 ? <p className="tts-hint">No projects</p> : (
              <div className="project-list">
                {projects.map(p => (
                  <div key={p.filename} className="project-item">
                    <div className="project-info"><strong>{p.name}</strong><span className="project-meta">{p.scene_count} scenes / {p.total_duration?.toFixed(1)}s</span></div>
                    <div className="project-actions">
                      <button className="btn-small" onClick={() => handleLoadProject(p.filename)}>Open</button>
                      <button className="btn-small" onClick={() => handleDuplicateProject(p.filename)}>Copy</button>
                      <button className="btn-tiny" onClick={() => handleDeleteProject(p.filename)}>Del</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
            <div className="modal-actions" style={{ marginTop: 12 }}><button className="btn-small" onClick={() => setShowProjectList(false)}>Close</button></div>
          </div>
        </div>
      )}

      {showTemplateSave && (
        <div className="modal-overlay" onClick={() => setShowTemplateSave(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h3>Save Template</h3>
            <input type="text" placeholder="Template name" value={templateName} onChange={e => setTemplateName(e.target.value)} className="modal-input" autoFocus />
            <div className="modal-actions">
              <button className="btn-primary" onClick={handleSaveTemplate} disabled={!templateName.trim()}>Save</button>
              <button className="btn-small" onClick={() => setShowTemplateSave(false)}>Cancel</button>
            </div>
            {templates.length > 0 && (
              <div className="template-list"><h4>Existing</h4>
                {templates.map(t => (
                  <div key={t.filename} className="template-item"><span>{t.name}</span>
                    <button className="btn-tiny" onClick={() => handleDeleteTemplate(t.filename)}>Del</button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {showPreview && scenes.length > 0 && <Preview scenes={scenes} telopPresets={telopPresets} onClose={() => setShowPreview(false)} />}
    </div>
  )
}

export default App
