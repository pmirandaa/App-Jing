import { useContext, useEffect, useRef, useState } from "react";
import { createSearchParams, useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

import MatchesSidebar from "components/sidebar/MatchesSidebar";
// import styles from "./Matches.module.css";
import SidebarPage from "pages/wrapper/SidebarPage";
import MatchesTable from "components/table/MatchesTable";
import LoadingOverlay from "components/loading/LoadingOverlay";
import { EventContext } from "contexts/EventContext";
import { useIsFirstRender, usePrevious } from "utils/hooks";
import { objectWithArraysToParams, paramsToObject } from "utils/utils";
import TablePagination from "components/pagination/TablePagination";

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
  const [pageSize, setPageSize] = useState(10);
  const [totalCount, setTotalCount] = useState(0);

  const rootRef = useRef();
  const isFirstRender = useIsFirstRender();

  function doSearch(params) {
    setIsLoading(true);
    const fetch = axios
      .get(`http://localhost:8000/api/matches/?${params.toString()}`)
      .then(sleeper(500))
      .then((response) => {
        setMatches(response.data.results);
        setTotalCount(response.data.count);
        rootRef.current.scrollTo(0, 0);
      })
      .finally(() => {
        setIsLoading(false);
      });
    return fetch;
  }

  useEffect(() => {
    if (isFirstRender) return;
    const searchFilters = { event: event, ...filters, page: currentPage };
    console.log(filters)
    if (currentPage != 1 && prevPage === currentPage) {
      setCurrentPage(1);
      return;
    }
    const searchParams = objectWithArraysToParams(searchFilters);
    const stringParams = searchParams.toString()
    const decodedParams = decodeURIComponent(stringParams)
    navigate("?" + decodedParams);

    doSearch(stringParams);
  }, [event, currentPage, filters]);

  useEffect(() => {
    const params = paramsToObject(location.search);
    const { page, ...filters } = params;
    if (page) setCurrentPage(page);
    setFilters(filters);
  }, []);

  const paginationEl = (
    <TablePagination
      current={currentPage}
      size={pageSize}
      count={totalCount}
      setCurrent={setCurrentPage}
      className="justify-content-center"
    />
  );

  return (
    <SidebarPage
      sidebar={<MatchesSidebar filters={filters} setFilters={setFilters} />}
      rootRef={rootRef}
    >
      <h1>Partidos</h1>
      <h4>Evento {event}</h4>
      {isLoading && <LoadingOverlay />}

      {matches.length > 0 ? (
        <>
          {paginationEl}
          <MatchesTable matches={matches} />
          {paginationEl}
        </>
      ) : (
        <p className="text-center lead">
          No se encontraron partidos con los criterios seleccionados
        </p>
      )}
    </SidebarPage>
  );
}
