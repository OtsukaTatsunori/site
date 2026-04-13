import { useState, useEffect } from 'react'
import './AssetPicker.css'

/**
 * 素材選択パネル（背景画像/動画、BGM）
 * props:
 *   assetType: "backgrounds" | "bgm"
 *   onSelect: (asset) => void  選択時のコールバック
 *   selectedPath: 現在選択中のパス
 */
export default function AssetPicker({ assetType, onSelect, selectedPath }) {
  const [assets, setAssets] = useState([])
  const [filterTag, setFilterTag] = useState('')
  const [playingAudio, setPlayingAudio] = useState(null)

  useEffect(() => {
    fetch(`/api/assets/${assetType}`)
      .then((res) => res.json())
      .then((data) => setAssets(data.assets || []))
      .catch((err) => console.error('素材取得エラー:', err))
  }, [assetType])

  // タグでフィルタ
  const filtered = filterTag
    ? assets.filter((a) => a.tags.some((t) => t.includes(filterTag)))
    : assets

  // 全タグ一覧を取得
  const allTags = [...new Set(assets.flatMap((a) => a.tags))]

  // BGMプレビュー再生
  const togglePlay = (path) => {
    if (playingAudio) {
      playingAudio.pause()
      playingAudio.currentTime = 0
      if (playingAudio._path === path) {
        setPlayingAudio(null)
        return
      }
    }
    const audio = new Audio(path)
    audio._path = path
    audio.play()
    audio.onended = () => setPlayingAudio(null)
    setPlayingAudio(audio)
  }

  const title = assetType === 'backgrounds' ? '背景素材' : 'BGM'

  return (
    <div className="asset-picker">
      <h3>{title}</h3>

      {/* タグフィルタ */}
      {allTags.length > 0 && (
        <div className="tag-filter">
          <button
            className={`tag-btn ${filterTag === '' ? 'active' : ''}`}
            onClick={() => setFilterTag('')}
          >
            すべて
          </button>
          {allTags.map((tag) => (
            <button
              key={tag}
              className={`tag-btn ${filterTag === tag ? 'active' : ''}`}
              onClick={() => setFilterTag(tag)}
            >
              {tag}
            </button>
          ))}
        </div>
      )}

      {/* 素材一覧 */}
      <div className="asset-grid">
        {/* 「なし」選択肢 */}
        <div
          className={`asset-item ${!selectedPath ? 'selected' : ''}`}
          onClick={() => onSelect(null)}
        >
          <div className="asset-thumb none-thumb">なし</div>
        </div>

        {filtered.map((asset) => (
          <div
            key={asset.filename}
            className={`asset-item ${selectedPath === asset.path ? 'selected' : ''}`}
            onClick={() => onSelect(asset)}
          >
            {asset.type === 'image' ? (
              <img
                className="asset-thumb"
                src={asset.path}
                alt={asset.filename}
                loading="lazy"
              />
            ) : asset.type === 'video' ? (
              <div className="asset-thumb video-thumb">
                <span>動画</span>
              </div>
            ) : (
              <div className="asset-thumb audio-thumb">
                <button
                  className="play-btn"
                  onClick={(e) => {
                    e.stopPropagation()
                    togglePlay(asset.path)
                  }}
                >
                  {playingAudio && playingAudio._path === asset.path ? '■' : '▶'}
                </button>
              </div>
            )}
            <span className="asset-name">{asset.filename}</span>
          </div>
        ))}
      </div>

      {filtered.length === 0 && assets.length === 0 && (
        <p className="no-assets">
          素材がありません。
          <br />
          assets/{assetType}/ にファイルを配置してください。
        </p>
      )}
    </div>
  )
}
