## 1. Scenario

I chose Scenario B, the investment club. The club wants to track what each member’s portfolios hold, when they buy and sell, and what their holdings are worth at the end of the day using closing prices. It also wants to keep track of ticker changes so it can follow the same asset over time. This would help the club review trading activity and compare portfolios.

## 2. ERD 

The first relationship to draw is: one member can own zero or more portfolios, and each portfolio belongs to exactly one member.

```mermaid
erDiagram
    MEMBERS ||--o{ PORTFOLIOS : owns

    MEMBERS {
        int member_id PK
        string first_name
        string last_name
        string email
        int class_year
        date join_date
    }

    PORTFOLIOS {
        int portfolio_id PK
        int member_id FK
        string name
        date created_date
        string strategy
    }

    PORTFOLIOS ||--o{ TRADES : records
    ASSETS ||--o{ TRADES : appears_in

    ASSETS {
        int asset_id PK
        string ticker
        string name
        string asset_type
        string sector
    }

    TRADES {
        int trade_id PK
        int portfolio_id FK
        int asset_id FK
        date trade_date
        string side
        decimal quantity
        decimal trade_price
        decimal fee 
        }
      ASSETS ||--o{ CLOSING_PRICES : has
    ASSETS ||--|{ TICKER_HISTORY : uses

    CLOSING_PRICES {
        int asset_id PK, FK
        date price_date PK
        decimal close_price
    }

    TICKER_HISTORY {
        int asset_id PK, FK
        date effective_from PK
        string ticker
    }
```

## 3. What One Row Means

| Table | What one row means |
| --- | --- |
| `MEMBERS` | One person in the club |
| `PORTFOLIOS` | One portfolio owned by one member |
| `ASSETS` | One investment that keeps the same ID even if its ticker changes |
| `TRADES` | One buy or sell of one asset in one portfolio on one date |
| `CLOSING_PRICES` | One asset’s closing price on one date |
| `TICKER_HISTORY` | One ticker for one asset, starting on the date it took effect |

## 4. Design Choices