import React from 'react';

export default function SkeletonCard() {
  return (
    <div className="flex flex-col rounded-md bg-card border border-wtr-border-muted overflow-hidden animate-pulse">
      <div className="aspect-3/4 w-full bg-muted/70" />
      <div className="p-3 flex flex-col flex-1 space-y-2">
        <div className="h-4 bg-muted/80 rounded w-3/4" />
        <div className="h-4 bg-muted/60 rounded w-1/2" />
        <div className="h-3 bg-muted/50 rounded w-1/3 mt-1" />
        <div className="flex items-center justify-between pt-2">
          <div className="h-4 bg-muted/60 rounded w-16" />
          <div className="h-4 bg-muted/60 rounded w-12" />
        </div>
        <div className="h-8 bg-muted/70 rounded w-full mt-auto" />
      </div>
    </div>
  );
}
