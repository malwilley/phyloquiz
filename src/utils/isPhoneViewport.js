const isPhoneViewport = () => {
  const viewportWidth = window.innerWidth

  return viewportWidth < 600
}

export default isPhoneViewport
