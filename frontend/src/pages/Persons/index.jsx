import PersonsSidebar from "pages/Persons/PersonsSidebar";
import PersonsTable from "pages/Persons/PersonsTable";
import TableSearchPage from "../wrapper/TableSearchPage";

export default function Persons() {
  return (
    <TableSearchPage
      SidebarComponent={PersonsSidebar}
      TableComponent={PersonsTable}
      apiName="persons"
      label="personas"
    />
  );
}
