import axios from "axios";
import FormSelect from "components/form/FormSelect";
import { EventContext } from "contexts/EventContext";
import { useContext, useEffect, useState } from "react";
import Form from "react-bootstrap/Form";
import Select from "react-select";
import { sleeper } from "utils/utils";

import styles from "./MatchesSidebar.module.css";

export default function MatchesSidebar({ filters, setFilters }) {
  const { event } = useContext(EventContext);
  const [participantsOptions, setParticipantsOptions] = useState([]);

  const updateFilters = (name, value) => {
    let newFilters = { ...filters };
    console.log(value, value == []);
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

  const handleMultiSelect = (options, action) => {
    const result = [];
    options.forEach((option) => {
      result.push(option.value);
    });
    console.log(result, action.name);
    updateFilters(action.name, result);
  };

  const participantsOptionsConstants = [
    { value: "1", label: "UAI STGO" },
    { value: "2", label: "PUC" },
    { value: "3", label: "UANDES" },
    { value: "4", label: "USM CC" },
    { value: "5", label: "UDEC" },
    { value: "6", label: "UAI VIÑA" },
    { value: "7", label: "USM STGO" },
    { value: "8", label: "UCH" },
  ];

  useEffect(() => {
    if (event === undefined) return;
    const fetch = axios
      .get(`http://localhost:8000/api/matches/filters/?event=${event}`)
      .then(sleeper(500))
      .then((response) => {
        const options = [];
        response.data.participants.forEach((element) => {
          options.push({ value: element.id, label: element.short_name });
        });
        setParticipantsOptions(options);
      })
      .finally(() => {
        //setIsLoading(false);
      });
  }, [event]);

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

      <Form.Label htmlFor="participants">Participantes</Form.Label>
      <Select
        isMulti
        placeholder="Sin filtrar"
        name="participants"
        inputId="participants"
        options={participantsOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleMultiSelect}
        value={participantsOptions.filter((o) => {
          if (filters.participants)
            return filters.participants.includes(o.value);
          else return false;
        })}
      />

      {/* <FormSelect
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
      </FormSelect> */}

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
