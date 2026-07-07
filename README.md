# Dida Hotel MCP — Hotel Search & Booking

[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](https://github.com/DIDA-AI/dida_hotel_mcp_global/releases)
[![ModelScope](https://img.shields.io/badge/ModelScope-Rank%237-brightgreen.svg)](https://modelscope.cn/)
[![Calls](https://img.shields.io/badge/Calls-847.3k-orange.svg)](https://github.com/DIDA-AI/dida_hotel_mcp_global)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

🏠 [Homepage](https://global.rollinggo.store/) · 🚀[ Quick Start](#-quick-start) · 🔧[ Tools](#tools) · 📚[ Examples](#usage-examples) · 💬[ Support](#-support)



## Why Dida Hotel MCP?

**Dida Hotel MCP** provides AI agents and MCP clients with hotel booking capabilities, designed for developers, AI builders, travel product teams, and enterprise travel scenarios who want to integrate hotel transaction functionality into their AI products. **Both enterprises and individuals can access it completely free with one-click setup.**

Official product backed by Asia's #1 and world's #3 B2B travel platform, DIDA, transforming AI "asking about hotels" into "completing full hotel booking workflows":

- **2 Million Global Hotels**: Coverage of all major global destinations
- **110K+ Direct Partner Hotels**: Real-time price and inventory responses
- **500+ Global Suppliers**: Covering global, regional, and local hotel brands to meet diverse user needs



## Who Is This For?

- Individual users with hotel search, price comparison, or flight monitoring needs
- Teams or developers building AI agents
- Developers looking to integrate hotel booking capabilities into MCP clients
- Developers building travel planning, business travel management, OTA, or lifestyle service agents
- Product teams validating AI agent business transaction workflows



## What Is This For?

- **General AI Agents**: Enable your agents with direct hotel booking capabilities, allowing users to complete workflows from demand understanding, intelligent recommendations, price comparison to order in natural conversation
- **AI Travel Assistant**: Intelligently recommend hotels based on user destinations, dates, budgets, and preferences, supporting multi-dimensional requirement matching
- **MCP / Agent Demo**: Students/learners quickly validate "AI agents directly completing hotel transactions" capabilities, building complete, demonstrable workflows
- Integrate hotel capabilities into **Claude, Cursor, Cherry Studio, ChatGPT MCP Client** or other MCP-compliant clients

⚠️ **Note**: If you're using platforms like ClawHub, DingXiang, or Qclaw, please use our [RollingGo Flight & Hotel Booking Skill](https://rollinggo.store/docs/skill-docs/skill-config) for details.



## 🚀 Quick Start

> 💡 In summary, you only need to do two things: apply for an API Key and configure it in your AI assistant. **No coding required** – any MCP-compliant AI assistant gains hotel search capabilities in 5 minutes with your first tool call.

### Step 1: Get Your API Key

1. [Visit the Application Page](https://global.rollinggo.store/apply)
2. Fill in basic information – automatic approval within 1-3 minutes. You'll receive an email containing:
   - API Key
   - Partner Center account (login + initial password) to configure markups, view orders, and check earnings
3. ⚠️ Check your email (including spam folder) for the API Key
4. **Limited-Time Offer**: All developers who complete their first tool call within 3 days of receiving the API Key unlock **permanent unlimited free access**. We prioritize developers with real needs and execution speed, offering zero-cost access to complete hotel MCP capabilities.

> The email includes both hotel and flight MCP endpoints – 1 key for both.



**Why Do We Require Information for API Key Application?**

Since hotel prices, inventory, and order capabilities involve real transaction workflows, we need to provision **free, dedicated keys for each developer**. This approach helps us:

- Provision appropriate access permissions for free
- Provide technical support during integration
- Understand your use case and reduce invalid configuration costs
- Protect API stability and prevent malicious calls or unusual traffic
- Quickly contact you about test orders, price queries, and inventory validation

We only use this information for key provisioning, integration support, and service security.


### Step 2: Setup & Running

### 1. Clone the Repository

```bash
git clone https://github.com/DIDA-AI/dida_hotel_mcp_global.git dida_hotel_mcp_global
cd dida_hotel_mcp_global
```

### 2. Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

### 3. Start the Server

```bash
python server.py
```

Default MCP endpoint: `http://127.0.0.1:8000/mcp`

The local server forwards tool calls to the RollingGo backend at `https://mcp.rollinggo.ai/mcp` using your API key.

### 4. Pass API Key via Headers in MCP Client

The server does **not** read the API Key from `.env`. Configure request headers in your MCP client:

- Recommended: `Authorization: Bearer YOUR_API_KEY`
- Alternative: `X-Secret-Key: YOUR_API_KEY`

> **Important:**
> - Apply for an API Key at https://global.rollinggo.store/apply
> - API Keys must start with `mcp_`
> - Missing or malformed keys will cause request failures

## MCP Client Configuration

```json
{
  "mcpServers": {
    "Dida-Hotel-MCP": {
      "url": "http://localhost:8000/mcp",
      "type": "http",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY",
        "Accept-Language": "en_US"
      }
    }
  }
}
```



## Tools

The server provides 3 tools:

1. `searchHotels` — Search hotels by location, dates, star rating, guest count, tags, etc.
2. `getHotelDetail` — Get real-time room types and pricing for a specific hotel
3. `getHotelSearchTags` — Retrieve tag metadata usable in `searchHotels.hotelTags`

### 1) searchHotels

#### Input Parameters

- `originQuery` (string, **required**): The user's original query.
- `place` (string, **required**): Location name — be as specific as possible (city / airport / attraction / detailed address, etc.).
- `placeType` (string, **required**): Location type. Supported values: `city`, `airport`, `point_of_interest`, `train_station`, `subway_station`, `hotel`, `district/county`, `detailed address`.
- `countryCode` (string, optional): ISO 3166-1 alpha-2 country code, e.g. `CN`, `US`.
- `size` (number, optional, default: `5`): Number of hotels to return, max `20`.
- `checkInParam` (object, optional): Check-in related parameters.
- `filterOptions` (object, optional): Filter parameters.
- `hotelTags` (object, optional): Tag / brand / budget filters.

**`checkInParam` fields:**

- `adultCount` (number, optional, default: `2`): Adults per room.
- `checkInDate` (string, optional, format: `YYYY-MM-DD`): Check-in date. If omitted, in the past, or malformed, defaults to tomorrow.
- `stayNights` (number, optional, default: `1`): Number of nights (max 28).

**`filterOptions` fields:**

- `distanceInMeter` (number, optional): Straight-line distance from POI in meters. Defaults to `2000` when a POI is used.
- `starRatings` (number[], optional): Star rating range, defaults to `[0.0, 5.0]`, step `0.5`.

**`hotelTags` fields:**

- `requiredTags` (string[], optional): Required tags (hard constraint).
- `preferredBrands` (string[], optional): Preferred brands.
- `maxPricePerNight` (number, optional): Max budget per night (CNY).

#### Output

```json
{
  "message": "Hotel search succeeded",
  "hotelInformationList": [
    {
      "hotelId": 43615,
      "bookingUrl": "https://rollinggo.cn/pages/hotel/detail/index?...",
      "name": "Sunworld Dynasty Hotel Beijing",
      "brand": null,
      "address": "50 Wangfujing Street",
      "destinationId": "6140156",
      "latitude": 39.917748,
      "longitude": 116.412249,
      "distanceInMeters": 205,
      "starRating": 5.0,
      "price": {
        "message": "Price found, lowest: 626.0, currency: CNY",
        "hasPrice": true,
        "currency": "CNY",
        "lowestPrice": 626.0
      },
      "areaCode": "CN",
      "description": "...",
      "imageUrl": "https://image-cdn.RollingGo.com/...",
      "hotelAmenities": ["24h Front Desk", "WiFi"],
      "score": 1.0,
      "tags": ["Near Shopping Mall", "Free WiFi"]
    }
  ]
}
```

> **Note:** `price` is an object, not a number. Fields may be missing or `null` depending on city/supply source.



### 2) getHotelDetail

#### Input Parameters

- `hotelId` (number, optional): Hotel ID. Mutually exclusive with `name`; if both are provided, `hotelId` takes priority.
- `name` (string, optional): Hotel name (fuzzy match).
- `dateParam` (object, optional): Check-in / check-out date parameters.
- `occupancyParam` (object, optional): Guest count and room count parameters.
- `localeParam` (object, optional): Country and currency parameters.

**`dateParam` fields:**

- `checkInDate` (string, optional, format: `YYYY-MM-DD`): Check-in date. Defaults to tomorrow if empty, malformed, or in the past.
- `checkOutDate` (string, optional, format: `YYYY-MM-DD`): Check-out date. Defaults to `checkInDate + 1` day if empty, malformed, or not after check-in.

**`occupancyParam` fields:**

- `adultCount` (number, optional, default: `2`): Adults per room.
- `childCount` (number, optional, default: `0`): Children per room.
- `childAgeDetails` (number[], optional): Child ages, e.g. `[3, 5]`.
- `roomCount` (number, optional, default: `1`): Number of rooms.

**`localeParam` fields:**

- `countryCode` (string, optional, default: `CN`): ISO 3166-1 alpha-2 country code.
- `currency` (string, optional, default: `USD`): Currency code.

#### Output

```json
{
  "success": true,
  "errorMessage": null,
  "hotelId": 43615,
  "bookingUrl": "https://rollinggo.cn/pages/hotel/detail/index?...",
  "name": "Sunworld Dynasty Hotel Beijing",
  "checkIn": "2026-03-05",
  "checkOut": "2026-03-06",
  "roomRatePlans": [
    {
      "roomTypeId": 4984714,
      "roomName": "Superior Room",
      "roomNameCn": "高级客房",
      "ratePlanId": "7012072001634754626",
      "ratePlanName": "Superior Room King Bed, 1 King Bed",
      "bedType": 73,
      "bedTypeDescription": "Unknown",
      "currency": "CNY",
      "totalPrice": 0,
      "totalSalesRate": null,
      "inventoryCount": null,
      "isOnRequest": null,
      "recommendIndex": null,
      "cancellationPolicies": [
        {
          "fromDate": "2026-03-02T10:00:00+08:00",
          "toDate": null,
          "amount": 634,
          "percent": null,
          "type": null,
          "description": null
        }
      ],
      "includedFees": null,
      "excludedFees": null,
      "metadata": null
    }
  ]
}
```

> **Note:** On failure, the response may contain an error message (e.g. "Failed to fetch pricing, please retry later") or structured error fields. The `roomRatePlans` array can be long — consider paginating or limiting display on the client side.



### 3) getHotelSearchTags

Retrieves available tags for use in `searchHotels.hotelTags`. Suitable for local caching and client-side intent mapping.

#### Output

```json
{
  "tags": [
    {
      "name": "Free WiFi",
      "category": "Core Amenities",
      "description": "Provides free WiFi"
    }
  ],
  "usageGuide": {
    "tagUsage": "Place tag names into hotelTags.preferredTags (preference), requiredTags (hard requirement), or excludedTags (exclusion)",
    "exampleRequest": "{...}"
  }
}
```

**Common tag categories:**

- Brand & Ratings
- Specialty Highlights
- Core Amenities
- Family & Kids
- Service Details
- Service & Dining
- Transportation & Payment
- Views & Room Types
- Hotel Type
- Pricing



## Usage Examples

### Example 1: City Search

```json
{
  "originQuery": "Find 4-star+ hotels in Beijing for 2 nights",
  "place": "Beijing",
  "placeType": "city",
  "checkInParam": {
    "checkInDate": "2026-03-01",
    "stayNights": 2
  },
  "filterOptions": {
    "starRatings": [4.0, 5.0]
  },
  "size": 5
}
```

### Example 2: With Tags and Budget Constraints

```json
{
  "originQuery": "Find quality hotels in Beijing with free WiFi, budget under 1000 per night",
  "place": "Beijing",
  "placeType": "city",
  "hotelTags": {
    "requiredTags": ["Free WiFi"],
    "maxPricePerNight": 1000
  },
  "size": 5
}
```

### Example 3: Query Hotel Room Types and Pricing

```json
{
  "hotelId": 43615,
  "dateParam": {
    "checkInDate": "2026-03-05",
    "checkOutDate": "2026-03-06"
  },
  "occupancyParam": {
    "adultCount": 2,
    "roomCount": 1
  },
  "localeParam": {
    "currency": "CNY",
    "countryCode": "CN"
  }
}
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



## 💬 Support
📧 Email: [york.lu@dida.com](mailto:york.lu@dida.com)

### Scan to Join WeChat Group for Technical Support

![Support WeChat](support-wehcat%20group.png)


Developer team is online to help you with:
- ✅ Integration configuration guidance
- ✅ API / MCP troubleshooting
- ✅ Hotel search, pricing, and booking workflow explanations
- ✅ Integration suggestions for your use case


**Made with ❤️ by Dida Team**
