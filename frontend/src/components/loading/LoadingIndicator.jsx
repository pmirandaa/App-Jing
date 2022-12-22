import { SwitchTransition, CSSTransition } from "react-transition-group";
import { Spinner } from "react-bootstrap";
import styles from "./LoadingIndicator.module.css";

export default function LoadingIndicator(props) {
  return (
    <SwitchTransition>
      <CSSTransition key={props.isLoading} classNames="fade" timeout={200}>
        {props.isLoading ? (
          <Spinner animation="border" variant="secondary" className={styles.spinner} />
        ) : (
          <></>
        )}
      </CSSTransition>
    </SwitchTransition>
  );
}
