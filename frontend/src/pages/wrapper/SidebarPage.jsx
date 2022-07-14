import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import styles from "./SidebarPage.module.css";

export default function SidebarPage(props) {
  return (
    <Container fluid className={styles.root}>
      <Row className={styles.wrapper}>
        <Col xs="2" className={styles.sidebar}>
            {props.sidebar}
        </Col>

        <Col className={styles.content}>
          {props.children}
        </Col>
      </Row>
    </Container>
  );
}
