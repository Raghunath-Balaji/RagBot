import React from "react";
import { Skeleton } from "./Skeleton";

export const ChatBubbleSkeleton = () => {
  return (
    <div className="flex flex-col space-y-6 w-full max-w-4xl mx-auto px-4 py-6">
      {/* User message skeleton */}
      <div className="flex justify-end">
        <div className="flex max-w-[80%] gap-3 flex-row-reverse">
          <Skeleton className="w-8 h-8 rounded-full shrink-0" />
          <div className="space-y-2">
            <Skeleton className="h-10 w-48 rounded-2xl rounded-tr-none" />
          </div>
        </div>
      </div>

      {/* Assistant message skeleton */}
      <div className="flex justify-start">
        <div className="flex max-w-[80%] gap-3">
          <Skeleton className="w-8 h-8 rounded-full shrink-0" />
          <div className="space-y-2">
            <Skeleton className="h-12 w-64 rounded-2xl rounded-tl-none" />
            <Skeleton className="h-8 w-40 rounded-2xl rounded-tl-none" />
          </div>
        </div>
      </div>

      {/* Another user message skeleton */}
      <div className="flex justify-end">
        <div className="flex max-w-[80%] gap-3 flex-row-reverse">
          <Skeleton className="w-8 h-8 rounded-full shrink-0" />
          <Skeleton className="h-10 w-32 rounded-2xl rounded-tr-none" />
        </div>
      </div>
    </div>
  );
};
