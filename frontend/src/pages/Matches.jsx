import { useContext, useEffect, useState } from "react";
import {
  createSearchParams,
  useLocation,
  useNavigate,
} from "react-router-dom";
import axios from "axios";

import MatchesSidebar from "components/sidebar/MatchesSidebar";
// import styles from "./Matches.module.css";
import SidebarPage from "pages/wrapper/SidebarPage";
import MatchesTable from "components/table/MatchesTable";
import LoadingOverlay from "components/loading/LoadingOverlay";
import { EventContext } from "contexts/EventContext";
import {
  useIsFirstRender,
  usePrevious,
} from "utils/hooks";
import { paramsToObject } from "utils/utils";

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
  const location = useLocation();
  const navigate = useNavigate();

  const [currentPage, setCurrentPage] = useState(1);
  const prevPage = usePrevious(currentPage);
  // const [pageSize, setPageSize] = useState(10);
  const [_, setTotalCount] = useState(0);

  const isFirstRender = useIsFirstRender();

  function doSearch(params) {
    setIsLoading(true);
    const fetch = axios
      .get(`http://localhost:8000/api/matches/?${params.toString()}`)
      .then(sleeper(500))
      .then((response) => {
        setMatches(response.data.results);
        setTotalCount(response.data.count);
      })
      .finally(() => {
        setIsLoading(false);
      });
    return fetch;
  }

  useEffect(() => {
    if (isFirstRender) return;
    let searchFilters = { event: event, ...filters, page: currentPage };
    if (prevPage === currentPage || prevPage === undefined)
      searchFilters["page"] = 1;

    let searchParams = createSearchParams(searchFilters);
    navigate("?" + searchParams.toString());

    doSearch(searchParams);
  }, [event, currentPage, filters]);

  useEffect(() => {
    const params = paramsToObject(location.search);
    const { page, ...filters } = params;
    if (page) setCurrentPage(page);
    setFilters(filters);
  }, []);

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
        <p className="text-center lead">
          No se encontraron partidos con los criterios seleccionados
        </p>
      )}
    </SidebarPage>
  );
}
