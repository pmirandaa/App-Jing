import axios from "axios";
import { API_URL } from "constants";
import { EventContext } from "contexts/EventContext";
import { useContext, useEffect, useState } from "react";
import { Container, Form, Table } from "react-bootstrap";
import Select from "react-select";
import { sleeper } from "utils";
import { useNavigate } from "react-router-dom";
import LoadingIndicator from "components/loading/LoadingIndicator";
import styles from "./Events.module.scss";
import { HouseFill, Trophy, TrophyFill } from "react-bootstrap-icons";

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
      .get(`${API_URL}/events/`)
      .then(sleeper(500))
      .then((response) => {
        console.log(response.data);
        console.log("index file");
        const res =
          response.data?.map((eve) => ({
            value: eve.id,
            label: eve.name,
            data: eve,
          })) ?? [];
        setEventOptions(res.reverse());
      })
      .finally(() => {
        //setIsLoading(false);
      });
  }, []);

  return (
    <Container style={{ padding: "16px", position: "relative" }}>
      <h1>Seleccionar evento</h1>
      <LoadingIndicator isLoading={isLoading} />

      <div className={styles.eventsContainer}>
        {eventOptions.map((eve) => (
          <div className={styles.eventCard} key={eve.value}>
            <img className={styles.eventLogo} src="/img/logoJING2019.jpg" />
            <p className={styles.eventLabel}>{eve.label}</p>
            <div className={styles.eventWinner}>
              <HouseFill className={styles.eventIcon2} />
              <span className={styles.eventWinnerLabel}>UCH</span>
              {eve.data.id === 10 ? (
                <span className={styles.eventActiveLabel}>En curso</span>
              ) : (
                <>
                  <TrophyFill className={styles.eventIcon} />
                  <span className={styles.eventWinnerLabel}>UCH</span>
                </>
              )}
            </div>
          </div>
        ))}
      </div>
    </Container>
  );
}
