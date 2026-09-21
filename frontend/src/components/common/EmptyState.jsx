import { Box, Button, Typography } from "@mui/material";

function EmptyState({
  icon,
  title = "No data found",
  description = "There is nothing to show right now.",
  actionLabel,
  onAction,
  actionTo,
  component,
}) {
  return (
    <Box className="flex min-h-72 flex-col items-center justify-center p-8 text-center">
      {icon && (
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-3xl bg-indigo-100 text-indigo-600">
          {icon}
        </div>
      )}

      <Typography variant="h6" className="font-bold">
        {title}
      </Typography>

      <Typography color="text.secondary" className="mt-2 max-w-md">
        {description}
      </Typography>

      {actionLabel && (
        <Button
          component={component}
          to={actionTo}
          variant="contained"
          className="mt-5"
          onClick={onAction}
        >
          {actionLabel}
        </Button>
      )}
    </Box>
  );
}

export default EmptyState;