import { Spinner } from "react-bootstrap";
import styles from "./LoadingOverlay.module.css";

export default function LoadingOverlay(props) {
  return (
    <div className={styles.root}>
        <Spinner animation="border" role="status" className={styles.spinner} {...props.spinnerProps}/>
    </div>
  );
}
