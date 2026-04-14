import { useState, useEffect, useRef } from 'react'
import './Preview.css'

export default function Preview({ scenes, telopPresets, onClose }) {
  const [playing, setPlaying] = useState(false)
  const [currentIdx, setCurrentIdx] = useState(0)
  const [elapsed, setElapsed] = useState(0)
  const [telopVisible, setTelopVisible] = useState(false)
  const timerRef = useRef(null)
  const startTimeRef = useRef(null)

  const totalDuration = scenes.reduce((sum, s) => sum + (s.duration || 0), 0)
  const sceneStarts = []
  let acc = 0
  for (const s of scenes) { sceneStarts.push(acc); acc += s.duration || 0 }

  useEffect(() => { return () => { if (timerRef.current) cancelAnimationFrame(timerRef.current) } }, [])

  const tick = () => {
    const t = (performance.now() - startTimeRef.current) / 1000
    if (t >= totalDuration) { setPlaying(false); setElapsed(totalDuration); setCurrentIdx(scenes.length - 1); return }
    setElapsed(t)
    let idx = 0
    for (let i = 0; i < sceneStarts.length; i++) { if (t >= sceneStarts[i]) idx = i }
    setCurrentIdx(idx)
    const se = t - sceneStarts[idx]
    const sd = scenes[idx]?.duration || 3
    setTelopVisible(se > 0.15 && se < sd - 0.15)
    timerRef.current = requestAnimationFrame(tick)
  }

  const handlePlay = () => {
    if (playing) { setPlaying(false); if (timerRef.current) cancelAnimationFrame(timerRef.current); return }
    setPlaying(true); setCurrentIdx(0); setElapsed(0)
    startTimeRef.current = performance.now()
    timerRef.current = requestAnimationFrame(tick)
  }

  const getStyle = (preset) => {
    const p = (telopPresets || []).find(t => t.id === preset) || {}
    return {
      fontSize: (p.fontsize || 48) * 0.35,
      color: p.fontcolor || 'white',
      WebkitTextStroke: `${(p.borderw || 2) * 0.4}px ${p.bordercolor || 'black'}`,
    }
  }

  const cs = scenes[currentIdx] || {}
  const progress = totalDuration > 0 ? (elapsed / totalDuration) * 100 : 0

  return (
    <div className="preview-overlay">
      <div className="preview-container">
        <div className="preview-header"><h3>Preview</h3><button className="btn-close" onClick={onClose}>Close</button></div>
        <div className="preview-screen">
          {cs.background ? <img src={cs.background} alt="" className="preview-screen-bg" /> : <div className="preview-screen-bg black" />}
          {cs.overlay_image && <img src={cs.overlay_image} alt="" style={{ position: 'absolute', width: '80%', top: '20%', zIndex: 1, objectFit: 'contain' }} />}
          <div className={`preview-screen-telop ${telopVisible ? 'visible' : ''}`} style={getStyle(cs.telop_style)}>{cs.text}</div>
          <div className="preview-scene-num">{currentIdx + 1} / {scenes.length}</div>
        </div>
        <div className="preview-controls">
          <button className="btn-play" onClick={handlePlay}>{playing ? 'Stop' : 'Play'}</button>
          <div className="preview-progress">
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progress}%` }} />
              {sceneStarts.slice(1).map((s, i) => <div key={i} className="scene-marker" style={{ left: `${(s / totalDuration) * 100}%` }} />)}
            </div>
            <span className="time-display">{elapsed.toFixed(1)}s / {totalDuration.toFixed(1)}s</span>
          </div>
        </div>
      </div>
    </div>
  )
}
