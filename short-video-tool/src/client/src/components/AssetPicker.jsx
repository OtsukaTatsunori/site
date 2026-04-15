import { useState, useEffect, useRef } from 'react'
import './AssetPicker.css'

export default function AssetPicker({ assetType, onSelect, selectedPath, label }) {
  const [assets, setAssets] = useState([])
  const [filterCat, setFilterCat] = useState('')
  const [playingAudio, setPlayingAudio] = useState(null)
  const fileRef = useRef()

  const reload = () => {
    fetch(`/api/assets/${assetType}`)
      .then(r => r.json())
      .then(d => setAssets(d.assets || []))
      .catch(() => {})
  }

  useEffect(() => { reload() }, [assetType])

  const categories = [...new Set(assets.map(a => a.category).filter(Boolean))]
  const filtered = filterCat ? assets.filter(a => a.category === filterCat) : assets

  const togglePlay = (path) => {
    if (playingAudio) { playingAudio.pause(); playingAudio.currentTime = 0; if (playingAudio._path === path) { setPlayingAudio(null); return } }
    const audio = new Audio(path); audio._path = path; audio.play(); audio.onended = () => setPlayingAudio(null); setPlayingAudio(audio)
  }

  const handleUpload = async (e) => {
    const files = e.target.files
    if (!files.length) return
    const formData = new FormData()
    for (const f of files) formData.append('files', f)
    formData.append('category', filterCat || '')
    await fetch(`/api/assets/${assetType}/upload`, { method: 'POST', body: formData })
    reload()
    e.target.value = ''
  }

  const title = label || (assetType === 'backgrounds' ? '背景' : assetType === 'bgm' ? 'BGM' : assetType === 'overlays' ? 'オーバーレイ' : assetType === 'se' ? '効果音' : assetType === 'fonts' ? 'フォント' : assetType)

  return (
    <div className="asset-picker">
      <div className="asset-picker-header">
        <h3>{title}</h3>
        <button className="btn-tiny" onClick={() => fileRef.current?.click()}>+ 追加</button>
        <input ref={fileRef} type="file" multiple accept="image/*,video/*,audio/*" onChange={handleUpload} style={{ display: 'none' }} />
      </div>

      {categories.length > 0 && (
        <div className="tag-filter">
          <button className={`tag-btn ${filterCat === '' ? 'active' : ''}`} onClick={() => setFilterCat('')}>全て</button>
          {categories.map(cat => (
            <button key={cat} className={`tag-btn ${filterCat === cat ? 'active' : ''}`} onClick={() => setFilterCat(cat)}>{cat}</button>
          ))}
        </div>
      )}

      <div className="asset-grid">
        <div className={`asset-item ${!selectedPath ? 'selected' : ''}`} onClick={() => onSelect(null)}>
          <div className="asset-thumb none-thumb">なし</div>
        </div>
        {filtered.map(asset => (
          <div key={asset.path} className={`asset-item ${selectedPath === asset.path ? 'selected' : ''}`} onClick={() => onSelect(asset)}>
            {asset.type === 'image' ? (
              <img className="asset-thumb" src={asset.path} alt={asset.filename} loading="lazy" />
            ) : asset.type === 'video' ? (
              <div className="asset-thumb video-thumb"><span>動画</span></div>
            ) : (
              <div className="asset-thumb audio-thumb">
                <button className="play-btn" onClick={e => { e.stopPropagation(); togglePlay(asset.path) }}>
                  {playingAudio && playingAudio._path === asset.path ? '||' : '>'}
                </button>
              </div>
            )}
            <span className="asset-name">{asset.filename}</span>
          </div>
        ))}
      </div>

      {filtered.length === 0 && assets.length === 0 && (
        <p className="no-assets">素材がありません。「+ 追加」からアップロードしてください。</p>
      )}
    </div>
  )
}
