import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import styles from "./SidebarPage.module.css";

export default function SidebarPage({sidebar, children, rootRef, ...props}) {
  return (
    <Container fluid className={styles.root} ref={rootRef} {...props}>
      <Row className={styles.wrapper}>
        <Col xs="2" className={styles.sidebar}>
            {sidebar}
        </Col>

        <Col className={styles.content}>
          {children}
        </Col>
      </Row>
    </Container>
  );
}
