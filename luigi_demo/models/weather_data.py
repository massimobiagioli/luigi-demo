from dataclasses import dataclass, asdict


@dataclass
class WeatherForecast:
    detection_date: str
    detection_hour: int
    city: str
    province: str
    temperature: str
    precipitation: str
    humidity: str
    wind: str

