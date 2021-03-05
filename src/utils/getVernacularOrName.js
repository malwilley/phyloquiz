const capitalize = (str) => str?.[0].toUpperCase() + str.slice(1)

const getVernacularOrName = (classification) =>
  capitalize(classification?.vernacular ?? classification?.name ?? 'Unknown')

export default getVernacularOrName
