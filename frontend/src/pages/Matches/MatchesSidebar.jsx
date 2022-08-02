import axios from "axios";
import { EventContext } from "contexts/EventContext";
import { useContext, useEffect, useState } from "react";
import Form from "react-bootstrap/Form";
import Select from "react-select";
import { sleeper } from "utils";

export default function MatchesSidebar({ filters, setFilters }) {
  const { event } = useContext(EventContext);
  const [participantsOptions, setParticipantsOptions] = useState([]);
  const [stateOptions, setStateOptions] = useState([]);
  const [sportOptions, setSportOptions] = useState([]);
  const [locationOptions, setLocationOptions] = useState([]);

  const updateFilters = (name, value) => {
    let newFilters = { ...filters };
    if (!value || (Array.isArray(value) && value.length === 0)) {
      delete newFilters[name];
    } else {
      newFilters[name] = value;
    }
    setFilters(newFilters);
  };

  const handleChangeForm = (e) => {
    updateFilters(e.target.name, e.target.checked ?? e.target.value);
  };

  const handleSelect = (options, action) => {
    console.log(options, action)
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

  useEffect(() => {
    if (!event) return;
    const fetch = axios
      .get(`http://localhost:8000/api/matches/filters/?event=${event.id}`)
      .then(sleeper(500))
      .then((response) => {
        setParticipantsOptions(response.data.participants ?? []);
        setStateOptions(response.data.state ?? []);
        setSportOptions(response.data.sport ?? []);
        setLocationOptions(response.data.location ?? []);
        console.log(response.data.participants);
      })
      .finally(() => {
        //setIsLoading(false);
      });
  }, [event]);

  return (
    <div>
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

      <Form.Label htmlFor="participants">Participantes</Form.Label>
      <Select
        isMulti
        placeholder="Sin filtrar"
        name="participants"
        inputId="participants"
        options={participantsOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
        value={participantsOptions.filter((o) => {
          return Array.isArray(filters.participants)
            ? filters.participants.includes(o.value)
            : filters.participants === o.value;
        })}
      />

      <Form.Label htmlFor="state">Estado</Form.Label>
      <Select
        isClearable
        placeholder="Sin filtrar"
        name="state"
        inputId="state"
        options={stateOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
        value={stateOptions.find((o) => o.value === filters.state) ?? null}
      />

      <Form.Label htmlFor="sport">Deporte</Form.Label>
      <Select
        isClearable
        placeholder="Sin filtrar"
        name="sport"
        inputId="sport"
        options={sportOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
        value={sportOptions.find((o) => o.value === filters.sport) ?? null}
      />

      <Form.Label htmlFor="location">Lugar</Form.Label>
      <Select
        isClearable
        placeholder="Sin filtrar"
        name="location"
        inputId="location"
        options={locationOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
        value={locationOptions.find((o) => o.value === filters.location) ?? null}
      />
    </div>
  );
}
