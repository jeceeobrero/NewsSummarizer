import React from 'react';

const Pagination = ({ currentPage, totalPages, paginate }) => {
  const pageNumbers = [...Array(totalPages).keys()].map(i => i + 1);

  return (
    <nav>
     <ul className='pagination my-5 mx-auto float-right'>
        {pageNumbers.map(number => (
          <li key={number} className={`page-item${number === currentPage ? ' active' : ''}`}>
            <a onClick={() => paginate(number)} href={`#`} className='page-link'>
              {number}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Pagination;
