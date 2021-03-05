const isSmoothScrollingSupported = () =>
  'scrollBehavior' in document.documentElement.style

export default isSmoothScrollingSupported
