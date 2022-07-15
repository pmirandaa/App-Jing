import Form from "react-bootstrap/Form";

import styles from "./MatchesSidebar.module.css";

export default function MatchesSidebar(props) {
  const updateFilters = (name, value) => {
    let filters = { ...props.filters };
    if (!value) {
      delete filters[name];
    } else {
      filters[name] = value;
    }
    props.setFilters(filters);
  };

  const handleChangeForm = (e) => {
    console.log(e)
    updateFilters(e.target.name, e.target.checked ?? e.target.value)
  }

  return (
    <div className={styles.root}>
      <Form.Group className="mb-3" controlId="filterMyMatches">
        <Form>
          <Form.Check
            name="my_matches"
            type="switch"
            label="Mostrar solo mis partidos"
            onChange={handleChangeForm}
          />
        </Form>
      </Form.Group>

      <Form.Group className="mb-3" controlId="filterParticipants">
        <Form.Label>Participantes</Form.Label>
        <Form.Select name="participants" onChange={handleChangeForm}>
          <option value="">Sin filtrar</option>
          <option value="1">UCH</option>
          <option value="2">PUC</option>
          <option value="3">UdeC</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className="mb-3" controlId="filterState">
        <Form.Label>Estado</Form.Label>
        <Form.Select name="state" onChange={handleChangeForm}>
          <option value="">Sin filtrar</option>
          <option value="MTB">MTB</option>
          <option value="MIC">MIC</option>
          <option value="MIF">MIF</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className="mb-3" controlId="filterSport">
        <Form.Label>Deporte</Form.Label>
        <Form.Select name="sport" onChange={handleChangeForm}>
          <option value="">Sin filtrar</option>
          <option value="1">Fútbol</option>
          <option value="2">Básquetbol</option>
        </Form.Select>
      </Form.Group>

      <Form.Group className="mb-3" controlId="filterLocation">
        <Form.Label>Lugar</Form.Label>
        <Form.Select name="location" onChange={handleChangeForm}>
          <option value="">Sin filtrar</option>
          <option value="1">La Cancha</option>
          <option value="2">Piscina</option>
        </Form.Select>
      </Form.Group>
    </div>
  );
}
