import { Card, CardContent, Skeleton } from "@mui/material";

function StatCardSkeleton() {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <Skeleton width="40%" height={24} />
            <Skeleton width="60%" height={48} />
            <Skeleton width="80%" height={24} />
          </div>

          <Skeleton variant="rounded" width={48} height={48} />
        </div>
      </CardContent>
    </Card>
  );
}

export default StatCardSkeleton;