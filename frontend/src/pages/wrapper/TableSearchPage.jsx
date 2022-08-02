import { useContext, useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

// import styles from "./Matches.module.css";
import SidebarPage from "pages/wrapper/SidebarPage";
import LoadingOverlay from "components/loading/LoadingOverlay";
import { EventContext } from "contexts/EventContext";
import { usePrevious } from "utils/hooks";
import { capitalize, objectWithArraysToParams, paramsToObject } from "utils";
import TablePagination from "components/pagination/TablePagination";

export default function TableSearchPage({
  SidebarComponent,
  TableComponent,
  apiUrl,
  label,
}) {
  const { event, setEvent } = useContext(EventContext);
  const [filters, setFilters] = useState({});
  const [rows, setRows] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [alreadyChanged, setAlreadyChanged] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const [currentPage, setCurrentPage] = useState(1);
  const prevPage = usePrevious(currentPage);
  const [pageSize /* , setPageSize */] = useState(10);
  const [totalCount, setTotalCount] = useState(0);

  const rootRef = useRef();
  const abortControllerRef = useRef(new AbortController());
  const pathnameRef = useRef(location.pathname);
  const keepLoading = useRef(false);

  useEffect(() => {
    return () => {
      abortControllerRef.current.abort();
    };
  }, []);

  useEffect(() => {
    if (!event || location.pathname !== pathnameRef.current) return;

    // Load filters from URL
    if (alreadyChanged) {
      setAlreadyChanged(false);
    } else {
      setAlreadyChanged(true);
      const params = paramsToObject(location.search);
      const { event: eventParam, page, ...filters } = params;
      if (eventParam) setEvent(eventParam);
      setCurrentPage(page ?? 1);
      setFilters(filters);
    }

    //// Fetch:
    // Abort previous request
    abortControllerRef.current.abort();
    abortControllerRef.current = new AbortController();
    // Prevent previous request from setting loading off when canceled
    if (isLoading) keepLoading.current = true;
    setIsLoading(true);
    axios
      .get(`http://localhost:8000${apiUrl}${location.search}`, {
        signal: abortControllerRef.current.signal,
      })
      .then((response) => {
        setRows(response.data.results);
        setTotalCount(response.data.count);
        rootRef.current.scrollTo(0, 0);
      })
      .finally(() => {
        if (!keepLoading.current) {
          setIsLoading(false);
        }
        keepLoading.current = false;
      })
      .catch((error) => {
        if (axios.isCancel(error)) {
          console.log("canceled");
        } else {
          throw error;
        }
      });
  }, [location.search]);

  useEffect(() => {
    if (!event) return;
    if (alreadyChanged) {
      setAlreadyChanged(false);
    } else {
      setAlreadyChanged(true);
      const searchFilters = { event: event.id, ...filters, page: currentPage };
      if (currentPage !== 1 && prevPage === currentPage) {
        setCurrentPage(1);
        return;
      }
      const searchParams = objectWithArraysToParams(searchFilters);
      const stringParams = searchParams.toString();
      const decodedParams = decodeURIComponent(stringParams);
      navigate("?" + decodedParams);
    }
  }, [event, currentPage, filters]);

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
      sidebar={<SidebarComponent filters={filters} setFilters={setFilters} />}
      rootRef={rootRef}
    >
      <h1>{capitalize(label)}</h1>
      <h4>{event?.name}</h4>
      {isLoading && <LoadingOverlay />}

      {rows.length > 0 ? (
        <>
          {paginationEl}
          <TableComponent rows={rows} />
          {paginationEl}
        </>
      ) : (
        <p className="text-center lead">
          No se encontraron {label} con los criterios seleccionados
        </p>
      )}

      {event === undefined && (
        <p className="text-center lead">No se ha seleccionado un evento</p>
      )}
    </SidebarPage>
  );
}
