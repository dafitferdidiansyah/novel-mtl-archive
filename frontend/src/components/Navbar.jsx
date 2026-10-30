import React from 'react';

export default function Navbar({ onOpenScan, searchQuery, onSearchChange, onSearchSubmit }) {
  return (
    <header className="border-bottom bg-white sticky-top shadow-xs">
      <nav className="navbar navbar-expand-lg navbar-light py-2">
        <div className="container-fluid px-3 px-md-4">
          {/* Brand Logo & MTL Subtitle */}
          <a className="navbar-brand d-flex align-items-center gap-2 m-0 text-decoration-none" href="/">
            <span className="badge bg-dark text-white rounded-pill px-3 py-1 fs-6 fw-bold shadow-xs">
              Novel MTL Archive
            </span>
            <span className="text-secondary fw-semibold small d-none d-sm-inline">
              RAW & Machine-Translated EPUBs
            </span>
          </a>

          {/* Quick Search in English */}
          <form className="d-flex mx-auto col-12 col-md-5 my-2 my-md-0" onSubmit={onSearchSubmit}>
            <div className="input-group input-group-sm w-100">
              <span className="input-group-text bg-light border-end-0 text-muted">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
              </span>
              <input
                className="form-control form-control-sm bg-light border-start-0"
                type="search"
                placeholder="Search novel title, raw original, or author..."
                aria-label="Search"
                value={searchQuery}
                onChange={(e) => onSearchChange(e.target.value)}
              />
            </div>
          </form>

          {/* Right Action: Clean scan button in English */}
          <div className="d-flex align-items-center">
            <button
              type="button"
              onClick={onOpenScan}
              className="btn btn-outline-dark btn-sm rounded-pill px-3 fw-medium"
              title="Scan local directory for ePub files"
            >
              + Scan Folder
            </button>
          </div>
        </div>
      </nav>
    </header>
  );
}
