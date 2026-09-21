import {
  Card,
  CardContent,
  Chip,
  Typography,
} from "@mui/material";

function SourceCard({ source, index }) {
  const filename = source.filename || source.file_name || "Unknown document";
  const chunkIndex = source.chunk_index ?? source.chunkIndex ?? "N/A";
  const score = source.similarity_score ?? source.score;
  const preview = source.preview || source.content || source.text || "";

  return (
    <Card variant="outlined" className="mb-3">
      <CardContent className="p-4">
        <div className="mb-3 flex flex-wrap items-center gap-2">
          <Chip label={`Source ${index + 1}`} size="small" color="primary" />
          <Chip label={filename} size="small" variant="outlined" />
          <Chip label={`Chunk ${chunkIndex}`} size="small" variant="outlined" />

          {score !== undefined && score !== null && (
            <Chip
              label={`Score: ${Number(score).toFixed(3)}`}
              size="small"
              variant="outlined"
            />
          )}
        </div>

        <Typography variant="body2" color="text.secondary">
          {preview || "No preview available."}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default SourceCard;