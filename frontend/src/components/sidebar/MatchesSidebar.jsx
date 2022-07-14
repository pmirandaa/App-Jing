import Form from "react-bootstrap/Form";

import styles from "./MatchesSidebar.module.css";

export default function MatchesSidebar(props) {
  const updateFilters = (name, value) => {
    props.setFilters((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleChangeParticipants = (e) => {
    updateFilters("participants", e.target.value);
  };

  const handleChangeState = (e) => {
    updateFilters("state", e.target.value);
  };

  const handleChangeMyMatches = (e) => {
    updateFilters("my_matches", e.target.value);
  };

  return (
    <div className={styles.root}>
      <Form.Group className="mb-3" controlId="filterMyMatches">
        <Form>
          <Form.Check
            type="switch"
            label="Buscar solo mis partidos"
            onChange={handleChangeMyMatches}
          />
        </Form>
      </Form.Group>

      <Form.Group className="mb-3" controlId="filterParticipants">
        <Form.Label>Participantes</Form.Label>
        <Form.Select onChange={handleChangeParticipants}>
          <option>Sin filtrar</option>
          <option value="1">One</option>
          <option value="2">Two</option>
          <option value="3">Three</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className="mb-3" controlId="filterState">
        <Form.Label>Estado</Form.Label>
        <Form.Select onChange={handleChangeState}>
          <option>Sin filtrar</option>
          <option value="MTB">MTB</option>
          <option value="MIC">MIC</option>
          <option value="MIF">MIF</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className="mb-3" controlId="filterSport">
        <Form.Label>Deporte</Form.Label>
        <Form.Select onChange={handleChangeState}>
          <option>Sin filtrar</option>
          <option value="a">A</option>
          <option value="b">B</option>
          <option value="c">C</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className="mb-3" controlId="filterLocation">
        <Form.Label>Lugar</Form.Label>
        <Form.Select onChange={handleChangeState}>
          <option>Sin filtrar</option>
          <option value="a">A</option>
          <option value="b">B</option>
          <option value="c">C</option>
        </Form.Select>
      </Form.Group>
    </div>
  );
}
