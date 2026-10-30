import React from 'react';
import { getDownloadUrl } from '../api';

export default function BookCard({ book, onOpenDetail }) {
  const coverUrl = book.cover || '/assets/cover_placeholder.svg';
  const genres = Array.isArray(book.genres) ? book.genres : [];
  const primaryGenre = genres[0] || 'Web Novel';
  const rawStatus = (book.status || 'Completed').toUpperCase();

  const handleDownload = (e) => {
    e.stopPropagation();
    window.location.href = getDownloadUrl(book.id);
  };

  return (
    <div className="col-12 col-md-6 mb-3">
      <div
        className="card card-clean-novel h-100 bg-white"
        onClick={() => onOpenDetail(book)}
      >
        <div className="row g-0 h-100">
          {/* Cover container */}
          <div className="col-4 col-sm-3 p-2 d-flex flex-column justify-content-between">
            <div className="ratio-cover-container">
              <img
                src={coverUrl}
                className="img-fluid rounded shadow-xs novel-cover-img"
                alt={book.title}
                loading="lazy"
                onError={(e) => {
                  e.currentTarget.onerror = null;
                  e.currentTarget.src = '/assets/cover_placeholder.svg';
                }}
              />
            </div>
            <div className="mt-2 text-center">
              <span className="badge bg-light text-muted border text-uppercase" style={{ fontSize: '10px' }}>
                {book.language || 'RAW/MTL'}
              </span>
            </div>
          </div>

          {/* Content info in English */}
          <div className="col-8 col-sm-9 d-flex flex-column">
            <div className="card-body p-3 d-flex flex-column justify-content-between h-100">
              <div>
                <div className="d-flex align-items-center gap-1 mb-1">
                  <span
                    className={`badge ${
                      rawStatus === 'COMPLETED' ? 'bg-success-subtle text-success border border-success-subtle' : 'bg-primary-subtle text-primary border border-primary-subtle'
                    }`}
                    style={{ fontSize: '10px' }}
                  >
                    {rawStatus}
                  </span>
                  <span className="badge bg-light text-secondary border" style={{ fontSize: '10px' }}>
                    {primaryGenre}
                  </span>
                </div>

                <h6 className="card-title fw-bold text-dark mb-1 text-truncate" title={book.title}>
                  {book.title}
                </h6>

                {book.original_title && (
                  <p className="text-muted small fst-italic text-truncate mb-1" style={{ fontSize: '11px' }}>
                    {book.original_title}
                  </p>
                )}

                <div className="d-flex align-items-center justify-content-between mb-2">
                  <p className="text-muted mb-0 text-truncate" style={{ fontSize: '11px', maxWidth: '70%' }}>
                    Author: <span className="fw-medium text-dark">{book.author || 'Anonymous'}</span>
                  </p>
                  {book.source_url && (
                    <a
                      href={book.source_url}
                      target="_blank"
                      rel="noreferrer"
                      className="badge bg-primary-subtle text-primary border border-primary-subtle text-decoration-none rounded-pill px-2 py-0"
                      style={{ fontSize: '9px' }}
                      title="Open Original Raw Source"
                      onClick={(e) => e.stopPropagation()}
                    >
                      RAW ↗
                    </a>
                  )}
                </div>

                <p
                  className="card-text text-secondary mb-2"
                  style={{
                    fontSize: '12px',
                    lineHeight: '1.45',
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden',
                  }}
                >
                  {book.description || 'Offline machine-translated (MTL) ePub archive ready for direct download.'}
                </p>
              </div>

              {/* Card footer details & action */}
              <div className="d-flex align-items-center justify-content-between pt-2 border-top">
                <span className="text-muted" style={{ fontSize: '11px' }}>
                  <b>{book.total_chapters}</b> Ch &bull; <b>{book.file_size_mb}</b> MB
                </span>
                <button
                  type="button"
                  onClick={handleDownload}
                  className="btn btn-dark btn-sm rounded-pill px-3 py-1 fw-medium"
                  style={{ fontSize: '11px' }}
                >
                  Download
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
