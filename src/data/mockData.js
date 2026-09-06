// Central mock dataset shared by every page.
// Coordinates are real neighborhoods/suburbs around Chennai so the map
// reads as a believable regional deployment rather than random points.

export const CHENNAI_CENTER = [13.0827, 80.2707]

export const EVENT_TYPES = [
  { key: 'rainfall', label: 'Rainfall', icon: '🌧️' },
  { key: 'flooding', label: 'Flooding / Waterlogging', icon: '🌊' },
  { key: 'thunderstorm', label: 'Thunderstorm & Lightning', icon: '⛈️' },
  { key: 'heatwave', label: 'Heatwave Condition', icon: '🌡️' },
  { key: 'fog', label: 'Fog & Smog', icon: '🌫️' },
  { key: 'dust', label: 'Dust Storm', icon: '💨' },
  { key: 'wind', label: 'High Wind & Storm Surge', icon: '🌀' },
]

export const STATUS = {
  VERIFIED: 'verified',
  REVIEW: 'review',
  FLAGGED: 'flagged',
}

// score 71-100 verified, 41-70 review (yellow zone), 0-40 flagged (red zone)
export const reports = [
  {
    id: 'WT-CHN-4821',
    title: 'Severe urban waterlogging & flash inundation',
    type: 'flooding',
    area: 'Kotturpuram, Chennai',
    lat: 13.0263, lng: 80.2437,
    score: 91,
    status: STATUS.VERIFIED,
    reportedAgo: '12 min ago',
    sources: 3,
    rainfallMm: 142,
    windKmh: 34,
    tempC: 27,
    thumb: 'https://images.unsplash.com/photo-1500674425229-f692875b0ab7?w=400&q=60',
    reporter: 'Ground Observer #A184',
    description: 'Waist-deep water reported along the arterial road near the bridge; buses rerouted, several two-wheelers stalled.',
  },
  {
    id: 'WT-CHN-4805',
    title: 'Heavy squall with lightning strikes',
    type: 'thunderstorm',
    area: 'Velachery, Chennai',
    lat: 12.9784, lng: 80.2209,
    score: 84,
    status: STATUS.VERIFIED,
    reportedAgo: '38 min ago',
    sources: 2,
    rainfallMm: 58,
    windKmh: 46,
    tempC: 26,
    thumb: 'https://images.unsplash.com/photo-1605727216801-e27ce1d0cc28?w=400&q=60',
    reporter: 'Ground Observer #A052',
    description: 'Continuous lightning over 20 minutes; residents advised to stay indoors near the lake bund road.',
  },
  {
    id: 'WT-CHN-4790',
    title: 'Localised waterlogging near IT corridor',
    type: 'flooding',
    area: 'Sholinganallur, Chennai',
    lat: 12.9010, lng: 80.2279,
    score: 63,
    status: STATUS.REVIEW,
    reportedAgo: '1 hr ago',
    sources: 1,
    rainfallMm: 39,
    windKmh: 21,
    tempC: 28,
    thumb: 'https://images.unsplash.com/photo-1603481546238-487240415921?w=400&q=60',
    reporter: 'Ground Observer #A233',
    description: 'Service lane flooded near the OMR junction; single report awaiting a second independent confirmation.',
  },
  {
    id: 'WT-CHN-4776',
    title: 'Rooftop wind-damage claim during storm surge',
    type: 'wind',
    area: 'Thiruvanmiyur, Chennai',
    lat: 12.9830, lng: 80.2591,
    score: 55,
    status: STATUS.REVIEW,
    reportedAgo: '1 hr 20 min ago',
    sources: 1,
    rainfallMm: 12,
    windKmh: 61,
    tempC: 27,
    thumb: 'https://images.unsplash.com/photo-1527482797697-8795b05a13fe?w=400&q=60',
    reporter: 'Ground Observer #A091',
    description: 'Photo shows sheet-metal roofing displaced; wind sensor confirmation pending from nearest ground station.',
  },
  {
    id: 'WT-CHN-4761',
    title: 'Coastal fog reducing visibility on ECR',
    type: 'fog',
    area: 'Injambakkam, Chennai',
    lat: 12.9210, lng: 80.2489,
    score: 47,
    status: STATUS.REVIEW,
    reportedAgo: '2 hr ago',
    sources: 1,
    rainfallMm: 0,
    windKmh: 9,
    tempC: 24,
    thumb: 'https://images.unsplash.com/photo-1487621167305-5d248087c724?w=400&q=60',
    reporter: 'Ground Observer #A014',
    description: 'Driver-submitted clip shows dense fog patch along the coast road early morning.',
  },
  {
    id: 'WT-CHN-4747',
    title: 'Tornado / dust vortex claim disputed',
    type: 'dust',
    area: 'Red Hills, Chennai',
    lat: 13.1930, lng: 80.1830,
    score: 22,
    status: STATUS.FLAGGED,
    reportedAgo: '3 hr ago',
    sources: 1,
    rainfallMm: 0,
    windKmh: 14,
    tempC: 33,
    thumb: 'https://images.unsplash.com/photo-1527482937786-6608f6c37cba?w=400&q=60',
    reporter: 'Ground Observer #A302',
    description: 'Claimed funnel cloud near the reservoir bund; IMD radar shows no rotation signature at the reported time.',
    factCheck: {
      claim: { rainfallMm: 0, windKmh: 88, note: 'Submission claims destructive rotating winds and structural damage across three streets.' },
      groundTruth: { rainfallMm: 0, windKmh: 14, note: 'Nearest IMD Doppler pass and two ground stations show only moderate gusting, no rotation signature.' },
      nearbyVerifiedCount: 0,
    },
  },
  {
    id: 'WT-CHN-4733',
    title: 'Extreme heatwave conditions reported',
    type: 'heatwave',
    area: 'Ambattur, Chennai',
    lat: 13.1143, lng: 80.1548,
    score: 78,
    status: STATUS.VERIFIED,
    reportedAgo: '4 hr ago',
    sources: 2,
    rainfallMm: 0,
    windKmh: 11,
    tempC: 41,
    thumb: 'https://images.unsplash.com/photo-1622278647071-92b76a86bcd8?w=400&q=60',
    reporter: 'Ground Observer #A067',
    description: 'Ambient temperature crossed 41°C at midday; matched against two nearby AWS ground stations.',
  },
  {
    id: 'WT-CHN-4718',
    title: 'Riverbank inundation near Adyar estuary',
    type: 'flooding',
    area: 'Kotturpuram, Chennai',
    lat: 13.0201, lng: 80.2517,
    score: 88,
    status: STATUS.VERIFIED,
    reportedAgo: '5 hr ago',
    sources: 3,
    rainfallMm: 96,
    windKmh: 29,
    tempC: 27,
    thumb: 'https://images.unsplash.com/photo-1547683905-f686c993aae5?w=400&q=60',
    reporter: 'Ground Observer #A140',
    description: 'Adyar river bank overflow reached the walking path; confirmed by three independent submissions.',
  },
  {
    id: 'WT-CHN-4702',
    title: 'Dust storm reducing highway visibility',
    type: 'dust',
    area: 'Sriperumbudur, Chennai Outskirts',
    lat: 12.9675, lng: 79.9427,
    score: 66,
    status: STATUS.REVIEW,
    reportedAgo: '6 hr ago',
    sources: 1,
    rainfallMm: 0,
    windKmh: 38,
    tempC: 34,
    thumb: 'https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=400&q=60',
    reporter: 'Ground Observer #A276',
    description: 'Highway dust haze reported near the industrial corridor; awaiting cross-source confirmation.',
  },
  {
    id: 'WT-CHN-4688',
    title: 'Thunderstorm with hail reported',
    type: 'thunderstorm',
    area: 'Tambaram, Chennai',
    lat: 12.9249, lng: 80.1000,
    score: 12,
    status: STATUS.FLAGGED,
    reportedAgo: '8 hr ago',
    sources: 1,
    rainfallMm: 4,
    windKmh: 19,
    tempC: 29,
    thumb: 'https://images.unsplash.com/photo-1500674425229-f692875b0ab7?w=400&q=60',
    reporter: 'Ground Observer #A399',
    description: 'Hail claim not corroborated by any ground station or nearby report; flagged for manual review.',
    factCheck: {
      claim: { rainfallMm: 40, windKmh: 55, note: 'Submission describes golf-ball sized hail and heavy rain over 15 minutes.' },
      groundTruth: { rainfallMm: 4, windKmh: 19, note: 'IMD station 3.1 km away recorded light rain only; no hail reports corroborated in the district.' },
      nearbyVerifiedCount: 0,
    },
  },
]

export const nearbyFor = (report) =>
  reports
    .filter((r) => r.id !== report.id && r.type === report.type)
    .slice(0, 3)

export const feedTicker = [
  { area: 'Perungudi, Chennai', type: 'flooding', ago: 'just now' },
  { area: 'Anna Nagar, Chennai', type: 'rainfall', ago: '2 min ago' },
  { area: 'Porur, Chennai', type: 'thunderstorm', ago: '4 min ago' },
  { area: 'Pallikaranai, Chennai', type: 'flooding', ago: '6 min ago' },
  { area: 'Guindy, Chennai', type: 'wind', ago: '9 min ago' },
]

export const districtVolumes = [
  { district: 'Chennai', reports: 18420, verifiedPct: 91 },
  { district: 'Coimbatore', reports: 6310, verifiedPct: 88 },
  { district: 'Madurai', reports: 5120, verifiedPct: 87 },
  { district: 'Tiruchirappalli', reports: 4042, verifiedPct: 89 },
  { district: 'Salem', reports: 3108, verifiedPct: 83 },
  { district: 'Kanchipuram', reports: 2894, verifiedPct: 90 },
]

export const dailyVolume = [
  { day: 'Mon', submitted: 612, verified: 540 },
  { day: 'Tue', submitted: 754, verified: 671 },
  { day: 'Wed', submitted: 690, verified: 615 },
  { day: 'Thu', submitted: 812, verified: 733 },
  { day: 'Fri', submitted: 940, verified: 842 },
  { day: 'Sat', submitted: 1120, verified: 1004 },
  { day: 'Sun', submitted: 980, verified: 878 },
]

export const typeBreakdown = [
  { type: 'Rainfall', count: 1128 },
  { type: 'Flooding / Waterlogging', count: 812 },
  { type: 'Thunderstorm & Lightning', count: 494 },
  { type: 'Heatwave Condition', count: 366 },
  { type: 'High Wind & Dust', count: 214 },
]

export function scoreZone(score) {
  if (score > 70) return STATUS.VERIFIED
  if (score >= 41) return STATUS.REVIEW
  return STATUS.FLAGGED
}
