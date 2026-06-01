import React from "react";
import { Skeleton } from "./Skeleton";

export const GlobalSkeleton = () => {
  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header Skeleton Mimic */}
      <div className="h-16 bg-white border-b border-gray-100 flex items-center px-6">
        <Skeleton className="h-8 w-32" />
        <div className="ml-auto flex gap-4">
          <Skeleton className="h-8 w-20" />
          <Skeleton className="h-8 w-20" />
        </div>
      </div>
      
      {/* Main Content Area Skeleton */}
      <main className="flex-1 p-8">
        <div className="max-w-4xl mx-auto space-y-8">
          <Skeleton className="h-12 w-1/3" />
          <div className="space-y-4">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-2/3" />
          </div>
          <div className="grid grid-cols-3 gap-6">
            <Skeleton className="h-32 rounded-xl" />
            <Skeleton className="h-32 rounded-xl" />
            <Skeleton className="h-32 rounded-xl" />
          </div>
        </div>
      </main>
    </div>
  );
};
