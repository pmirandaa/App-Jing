import { useState } from "react";
import Pagination from "react-bootstrap/Pagination";
import { clamp } from "utils/utils";

export default function TablePagination({
  current,
  size,
  count,
  setCurrent,
  ...props
}) {
  const totalPages = Math.ceil(count / size);
  
  let lowLimit = Math.max(Math.min(current - 4, totalPages - 8), 1);
  let highLimit = Math.min(lowLimit + 8, totalPages);

  const isEllipsisPrev = lowLimit > 1;
  const isEllipsisNext = highLimit < totalPages;
  if (isEllipsisPrev) lowLimit += 2;
  if (isEllipsisNext) highLimit -= 2;

  const pages = [];
  for (let i = lowLimit; i <= highLimit; i++) {
    pages.push(i);
  }

  return (
    <Pagination {...props}>
      <Pagination.Prev
        onClick={() => setCurrent(current - 1)}
        disabled={current <= 1}
      />

      {isEllipsisPrev && (
        <>
          <Pagination.Item onClick={() => setCurrent(1)}>{1}</Pagination.Item>
          <Pagination.Ellipsis disabled />
        </>
      )}

      {pages.map((page) => {
        return (
          <Pagination.Item
            onClick={() => setCurrent(page)}
            active={page == current}
            key={"page" + page}
          >
            {page}
          </Pagination.Item>
        );
      })}

      {isEllipsisNext && (
        <>
          <Pagination.Ellipsis disabled />
          <Pagination.Item onClick={() => setCurrent(totalPages)}>
            {totalPages}
          </Pagination.Item>
        </>
      )}

      <Pagination.Next
        onClick={() => setCurrent(+current + 1)}
        disabled={current >= totalPages}
      />
    </Pagination>
  );
}
