import PersonsSidebar from "pages/Persons/PersonsSidebar";
import PersonsTable from "pages/Persons/PersonsTable";
import TableSearchPage from "../wrapper/TableSearchPage";

export default function Persons() {
  return (
    <TableSearchPage
      SidebarComponent={PersonsSidebar}
      TableComponent={PersonsTable}
      apiUrl="/api/persons/"
      label="personas"
    />
  );
}
