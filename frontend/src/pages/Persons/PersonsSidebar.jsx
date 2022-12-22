import axios from "axios";
import { API_URL } from "constants";
import { EventContext } from "contexts/EventContext";
import { useContext, useEffect, useState } from "react";
import Form from "react-bootstrap/Form";
import Select from "react-select";
import { unaccent } from "utils";

export default function PersonsSidebar({ filters, setFilters }) {
  const { event } = useContext(EventContext);
  const [universityOptions, setUniversityOptions] = useState([]);
  const [sportOptions, setSportOptions] = useState([]);

  const updateFilters = (name, value) => {
    if (filters[name] === value || (filters[name] === undefined && value === "")) return;
    let newFilters = { ...filters };
    if (!value || (Array.isArray(value) && value.length === 0)) {
      delete newFilters[name];
    } else {
      newFilters[name] = value;
    }
    setFilters(newFilters);
  };

  const handleSelect = (options, action) => {
    if (Array.isArray(options)) {
      const result = [];
      options.forEach((option) => {
        result.push(option.value);
      });
      updateFilters(action.name, result);
    } else {
      updateFilters(action.name, options != null ? options.value : null);
    }
  };

  const handleCheckbox = (e) => {
    updateFilters(e.target.name, e.target.checked);
  };

  const handleText = (e) => {
    updateFilters(e.target.name, unaccent(e.target.value));
  };

  useEffect(() => {
    if (!event) return;
    const fetch = axios
      .get(`${API_URL}/persons/filters/?event=${event.id}`)
      .then((response) => {
        setUniversityOptions(response.data.university ?? []);
        setSportOptions(response.data.sport ?? []);
      })
      .finally(() => {
        //setIsLoading(false);
      });
  }, [event]);

  return (
    <div>
      <Form.Label htmlFor="first_name">Nombre</Form.Label>
      <Form.Control
        placeholder="Sin filtrar"
        name="first_name"
        onBlur={handleText}
        onKeyPress={(e) => {
          if (e.key === "Enter") handleText(e);
        }}
      />

      <Form.Label htmlFor="last_name">Apellido</Form.Label>
      <Form.Control
        placeholder="Sin filtrar"
        name="last_name"
        onBlur={handleText}
        onKeyPress={(e) => {
          if (e.key === "Enter") handleText(e);
        }}
      />

      <Form.Label htmlFor="university">Universidad</Form.Label>
      <Select
        isClearable
        placeholder="Sin filtrar"
        name="university"
        inputId="university"
        options={universityOptions}
        classNamePrefix="select"
        onChange={handleSelect}
        value={universityOptions.find((o) => o.value === filters.university) ?? null}
      />

      <Form.Label htmlFor="sport">Deporte</Form.Label>
      <Select
        isClearable
        isSearchable
        placeholder="Sin filtrar"
        name="sport"
        inputId="sport"
        options={sportOptions}
        onChange={handleSelect}
        value={sportOptions.find((o) => o.value === filters.sport) ?? null}
      />

      <Form.Check
        label="Coordinador deportivo"
        name="is_coord_sport"
        id="is_coord_sport"
        checked={filters.is_coord_sport}
        onChange={handleCheckbox}
      />

      <Form.Check
        label="Coordinador universitario"
        name="is_coord_uni"
        id="is_coord_uni"
        checked={filters.is_coord_uni}
        onChange={handleCheckbox}
      />

      <Form.Check
        label="Administrador"
        name="is_admin"
        id="is_admin"
        checked={filters.is_admin}
        onChange={handleCheckbox}
      />
    </div>
  );
}
