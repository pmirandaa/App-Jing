import { useContext, useEffect, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import axios from "axios";

import MatchesSidebar from "components/sidebar/MatchesSidebar";
import styles from "./Matches.module.css";
import SidebarPage from "pages/wrapper/SidebarPage";
import MatchesTable from "components/table/MatchesTable";
import LoadingOverlay from "components/loading/LoadingOverlay";
import { EventContext } from "contexts/EventContext";

function sleeper(ms) {
  return function (x) {
    return new Promise((resolve) => setTimeout(() => resolve(x), ms));
  };
}

export default function Matches() {
  const { event } = useContext(EventContext);
  const [filters, setFilters] = useState({});
  const [matches, setMatches] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();

  const firstUpdate = useRef(true);

  useEffect(() => {
    if (!firstUpdate.current) {
      setSearchParams(filters);
    } else {
      firstUpdate.current = false;
    }
  }, [filters]);

  useEffect(() => {
    setIsLoading(true);
    axios
      .get(
        `http://localhost:8000/api/matches/?event=${event}&${searchParams.toString()}`
      )
      .then(sleeper(500))
      .then((response) => {
        setMatches(response.data.results);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [searchParams, event]);

  return (
    <SidebarPage
      sidebar={<MatchesSidebar filters={filters} setFilters={setFilters} />}
    >
      <h1>Partidos</h1>
      <h4>Evento {event}</h4>
      {isLoading && <LoadingOverlay />}
      
      {matches.length > 0 ? (
        <MatchesTable matches={matches} />
      ) : (
        <p className="text-center lead">No se encontraron partidos con los criterios seleccionados</p>
      )}
    </SidebarPage>
  );
}
