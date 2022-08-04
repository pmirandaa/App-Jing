import Alert from "react-bootstrap/Alert";

export default function AlertTemplate({ style, options, message, close }) {
  let variant = options.type;
  if (variant === "info") variant = "primary";
  if (variant === "success") variant = "success";
  if (variant === "error") variant = "danger";
  return (
    <Alert variant={variant} style={style} onClose={close} dismissible>
      {message}
    </Alert>
  );
}
