import axios from "axios";
import { EventContext } from "contexts/EventContext";
import { useContext, useEffect, useState } from "react";
import { Container, Form, Table } from "react-bootstrap";
import Select from "react-select";
import { sleeper } from "utils";
import { useNavigate } from "react-router-dom";
import LoadingOverlay from "components/loading/LoadingOverlay";

export default function Events() {
  const { event, setEvent } = useContext(EventContext);
  const [eventOptions, setEventOptions] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  function handleSelect(option, action) {
    setIsLoading(true);
    setSelectedEvent(option);
    setEvent({ id: option.value, name: option.label });
    setTimeout(() => {
      setIsLoading(false);
      navigate("/");
    }, 1000);
  }

  useEffect(() => {
    const fetch = axios
      .get(`http://localhost:8000/api/events/`)
      .then(sleeper(500))
      .then((response) => {
        console.log(response.data);
        const res =
          response.data?.map((eve) => ({
            value: eve.id,
            label: eve.name,
            data: eve,
          })) ?? [];
        setEventOptions(res);
      })
      .finally(() => {
        //setIsLoading(false);
      });
  }, []);

  return (
    <Container style={{ padding: "16px", position: "relative" }}>
      <h1>Seleccionar evento</h1>

      <Form.Label htmlFor="event">Evento</Form.Label>
      <Select
        name="event"
        inputId="event"
        options={eventOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
        value={selectedEvent}
      />
      {isLoading && <LoadingOverlay />}
    </Container>
  );
}
