export type PublisherMini = {
  id: number;
  agency_name: string;
  verified: boolean;
  location: string;
  logo_url: string;
};

export type PublisherPublic = PublisherMini & {
  contact_name: string;
  email: string;
  phone: string;
  description: string;
  cars_count: number;
  suspended?: boolean;
};

export type CarCard = {
  id: number;
  brand: string;
  model: string;
  year: number;
  price_per_day: number;
  fuel: string;
  transmission: string;
  body_type: string;
  seats: number;
  location: string;
  views_count: number;
  primary_image: string | null;
  publisher: PublisherMini;
};

export type CarImage = { id: number; url: string; is_primary: boolean; sort_order: number };
export type AvailabilityBlock = { id: number; date_from: string; date_to: string; reason: string };

export type CarDetail = Omit<CarCard, "primary_image" | "publisher"> & {
  doors: number;
  mileage: number;
  description: string;
  features: string[];
  pickup_options: string;
  deposit_info: string;
  cancellation_policy: string;
  min_driver_age: number;
  images: CarImage[];
  availability_blocks: AvailabilityBlock[];
  publisher: PublisherPublic;
};

export type Inquiry = {
  id: number;
  car_id: number;
  publisher_id: number;
  pickup_date: string;
  return_date: string;
  pickup_location: string;
  full_name: string;
  phone: string;
  email: string;
  message: string;
  status: "PENDING" | "ANSWERED" | "CLOSED" | string;
  created_at: string;
  car_title: string;
  car_image: string | null;
};

export type UserMe = {
  id: number;
  email: string;
  role: "ADMIN" | "PUBLISHER" | string;
  full_name: string;
  phone: string;
  publisher_id: number | null;
};

export type HomePayload = {
  popular_cars: CarCard[];
  popular_locations: string[];
  featured_publishers: PublisherPublic[];
};

export type PublisherStats = {
  cars_count: number;
  active_cars: number;
  new_inquiries: number;
  total_inquiries: number;
  views_count: number;
};

export type SearchParams = {
  location?: string;
  pickup_date?: string;
  return_date?: string;
  brand?: string;
  model?: string;
  min_price?: string;
  max_price?: string;
  fuel?: string;
  transmission?: string;
  body_type?: string;
  seats?: string;
  year_from?: string;
  year_to?: string;
  q?: string;
  sort?: string;
};
