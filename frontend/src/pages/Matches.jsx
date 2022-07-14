import { useEffect, useState } from "react";
import axios from "axios";

import MatchesSidebar from "components/sidebar/MatchesSidebar";
import styles from "./Matches.module.css";
import SidebarPage from "pages/wrapper/SidebarPage";
import MatchesTable from "components/table/MatchesTable";
import LoadingOverlay from "components/loading/LoadingOverlay";

function sleeper(ms) {
  return function(x) {
    return new Promise(resolve => setTimeout(() => resolve(x), ms));
  };
}

export default function Matches() {
  const [filters, setFilters] = useState({});
  const [matches, setMatches] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    setIsLoading(true);
    axios
      .get("http://localhost:8000/api/matches/")
      .then(sleeper(1000))
      .then((response) => {
        setMatches(response.data.results);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [filters]);

  return (
    <SidebarPage
      sidebar={<MatchesSidebar filters={filters} setFilters={setFilters} />}
    >
      <h1>Partidos</h1>
      {isLoading && <LoadingOverlay />}
      <MatchesTable matches={matches} />
    </SidebarPage>
  );
}
