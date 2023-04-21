import React from 'react'

const NavItems = ({text, classes}) => {
  return (
    <button className={classes}>
      <li><a>{text}</a></li>
    </button>
  )
}

export default NavItems