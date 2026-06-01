import React from "react";
import { Skeleton } from "./Skeleton";

export const AdminTableSkeleton = () => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="bg-gray-50 border-b border-gray-200 h-12 flex items-center px-6 gap-8">
        <Skeleton className="h-4 w-1/4" />
        <Skeleton className="h-4 w-1/6" />
        <Skeleton className="h-4 w-1/6" />
        <Skeleton className="h-4 w-1/6 ml-auto" />
      </div>
      <div className="divide-y divide-gray-200">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="px-6 py-4 flex items-center gap-8">
            <div className="flex items-center gap-3 w-1/4">
              <Skeleton className="w-5 h-5 rounded" />
              <Skeleton className="h-4 w-32" />
            </div>
            <Skeleton className="h-4 w-1/6" />
            <Skeleton className="h-4 w-20" />
            <Skeleton className="h-8 w-8 rounded ml-auto" />
          </div>
        ))}
      </div>
    </div>
  );
};
