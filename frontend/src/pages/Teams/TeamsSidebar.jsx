import axios from "axios";
import { API_URL } from "constants";
import { EventContext } from "contexts/EventContext";
import { useContext, useEffect, useState } from "react";
import Form from "react-bootstrap/Form";
import Select from "react-select";
import { sleeper } from "utils";

export default function TeamsSidebar({ filters, setFilters }) {
  const { event } = useContext(EventContext);
  const [sportOptions, setSportOptions] = useState([]);
  const [universityOptions, setUniversityOptions] = useState([]);
  const [genderOptions, setGenderOptions] = useState([]);
  const [sportTypeOptions, setSportTypeOptions] = useState([]);

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
    console.log(options, action);
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
      .get(`${API_URL}/teams/filters/?event=${event.id}`)
      .then(sleeper(500))
      .then((response) => {
        setSportOptions(response.data.sport ?? []);
        setUniversityOptions(response.data.universities ?? []);
        setGenderOptions(response.data.gender ?? []);
        setSportTypeOptions(response.data.sport_type ?? []);
      })
      .finally(() => {
        //setIsLoading(false);
      });
  }, [event]);

  return (
    <div>
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

      <Form.Label htmlFor="gender">Género</Form.Label>
      <Select
        isClearable
        placeholder="Sin filtrar"
        name="gender"
        inputId="gender"
        options={genderOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
        value={genderOptions.find((o) => o.value === filters.gender) ?? null}
      />

      <Form.Label htmlFor="sport_type">Tipo de deporte</Form.Label>
      <Select
        isClearable
        placeholder="Sin filtrar"
        name="sport_type"
        inputId="sport_type"
        options={sportTypeOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
        value={
          sportTypeOptions.find((o) => o.value === filters.sport_type) ?? null
        }
      />
    </div>
  );
}
