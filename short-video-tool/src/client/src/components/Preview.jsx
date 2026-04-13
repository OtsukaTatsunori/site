import { useState, useEffect, useRef } from 'react'
import './Preview.css'

/**
 * 簡易プレビュー：シーンを順番に表示してテロップのタイミングを確認
 */
export default function Preview({ scenes, onClose }) {
  const [playing, setPlaying] = useState(false)
  const [currentIdx, setCurrentIdx] = useState(0)
  const [elapsed, setElapsed] = useState(0)
  const [telopVisible, setTelopVisible] = useState(false)
  const timerRef = useRef(null)
  const startTimeRef = useRef(null)
  const sceneStartRef = useRef(0)

  const totalDuration = scenes.reduce((sum, s) => sum + (s.duration || 0), 0)

  // 各シーンの開始時間を計算
  const sceneStarts = []
  let acc = 0
  for (const s of scenes) {
    sceneStarts.push(acc)
    acc += s.duration || 0
  }

  useEffect(() => {
    return () => {
      if (timerRef.current) cancelAnimationFrame(timerRef.current)
    }
  }, [])

  const tick = () => {
    const now = performance.now()
    const t = (now - startTimeRef.current) / 1000

    if (t >= totalDuration) {
      setPlaying(false)
      setElapsed(totalDuration)
      setCurrentIdx(scenes.length - 1)
      return
    }

    setElapsed(t)

    // 現在のシーンを特定
    let idx = 0
    for (let i = 0; i < sceneStarts.length; i++) {
      if (t >= sceneStarts[i]) idx = i
    }
    setCurrentIdx(idx)

    // テロップのフェード（0.3秒後に表示、終了0.3秒前にフェードアウト）
    const sceneElapsed = t - sceneStarts[idx]
    const sceneDuration = scenes[idx]?.duration || 3
    setTelopVisible(sceneElapsed > 0.15 && sceneElapsed < sceneDuration - 0.15)

    timerRef.current = requestAnimationFrame(tick)
  }

  const handlePlay = () => {
    if (playing) {
      // 停止
      setPlaying(false)
      if (timerRef.current) cancelAnimationFrame(timerRef.current)
      return
    }

    // 再生開始
    setPlaying(true)
    setCurrentIdx(0)
    setElapsed(0)
    startTimeRef.current = performance.now()
    timerRef.current = requestAnimationFrame(tick)
  }

  const currentScene = scenes[currentIdx] || {}
  const progress = totalDuration > 0 ? (elapsed / totalDuration) * 100 : 0

  return (
    <div className="preview-overlay">
      <div className="preview-container">
        <div className="preview-header">
          <h3>プレビュー</h3>
          <button className="btn-close" onClick={onClose}>閉じる</button>
        </div>

        <div className="preview-screen">
          {/* 背景 */}
          {currentScene.background ? (
            <img src={currentScene.background} alt="" className="preview-screen-bg" />
          ) : (
            <div className="preview-screen-bg black" />
          )}

          {/* テロップ */}
          <div className={`preview-screen-telop ${telopVisible ? 'visible' : ''}`}>
            {currentScene.text}
          </div>

          {/* シーン番号 */}
          <div className="preview-scene-num">
            {currentIdx + 1} / {scenes.length}
          </div>
        </div>

        {/* コントロール */}
        <div className="preview-controls">
          <button className="btn-play" onClick={handlePlay}>
            {playing ? '■ 停止' : '▶ 再生'}
          </button>
          <div className="preview-progress">
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progress}%` }} />
              {/* シーン区切り線 */}
              {sceneStarts.slice(1).map((start, i) => (
                <div key={i} className="scene-marker"
                  style={{ left: `${(start / totalDuration) * 100}%` }} />
              ))}
            </div>
            <span className="time-display">
              {elapsed.toFixed(1)}s / {totalDuration.toFixed(1)}s
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
