import FormSelect from "components/form/FormSelect";
import Form from "react-bootstrap/Form";

import styles from "./MatchesSidebar.module.css";

export default function MatchesSidebar({ filters, setFilters }) {
  const updateFilters = (name, value) => {
    let newFilters = { ...filters };
    if (!value) {
      delete newFilters[name];
    } else {
      newFilters[name] = value;
    }
    setFilters(newFilters);
  };

  const handleChangeForm = (e) => {
    updateFilters(e.target.name, e.target.checked ?? e.target.value);
  };

  return (
    <div className={styles.root}>
      <Form.Group className="mb-3" controlId="filterMyMatches">
        <Form>
          <Form.Check
            name="my_matches"
            type="switch"
            label="Mostrar solo mis partidos"
            onChange={handleChangeForm}
            checked={filters.my_matches}
          />
        </Form>
      </Form.Group>

      <FormSelect
        label="Participantes"
        name="participants"
        onChange={handleChangeForm}
        value={filters.participants}
      >
        <option value="">Sin filtrar</option>
        <option value="1">UAI STGO</option>
        <option value="2">PUC</option>
        <option value="3">UANDES</option>
        <option value="4">USM CC</option>
        <option value="5">UDEC</option>
        <option value="6">UAI VIÑA</option>
        <option value="7">USM STGO</option>
        <option value="8">UCH</option>
      </FormSelect>

      <FormSelect
        label="Estado"
        name="state"
        onChange={handleChangeForm}
        value={filters.state}
      >
      <option value="">Sin filtrar</option>
      <option value="MTB">MTB</option>
      <option value="MIC">MIC</option>
      <option value="MIF">MIF</option>
      </FormSelect>

      <FormSelect
        label="Deporte"
        name="sport"
        onChange={handleChangeForm}
        value={filters.sport}
      >
      <option value="">Sin filtrar</option>
      <option value="1">Fútbol</option>
      <option value="2">Básquetbol</option>
      </FormSelect>

      <FormSelect
        label="Lugar"
        name="location"
        onChange={handleChangeForm}
        value={filters.location}
      >
      <option value="">Sin filtrar</option>
      <option value="1">La Cancha</option>
      <option value="2">Piscina</option>
      </FormSelect>
    </div>
  );
}
