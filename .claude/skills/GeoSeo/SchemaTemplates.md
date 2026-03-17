# JSON-LD Schema Templates

Ready-to-use JSON-LD templates for GEO optimization. Replace bracketed values before implementation. All schemas must be server-rendered (not injected via JavaScript).

## Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[REPLACE: Your Company Name]",
  "url": "[REPLACE: https://yoursite.com]",
  "logo": "[REPLACE: https://yoursite.com/logo.png]",
  "description": "[REPLACE: Brief company description, 1-2 sentences]",
  "foundingDate": "[REPLACE: YYYY-MM-DD]",
  "sameAs": [
    "[REPLACE: https://en.wikipedia.org/wiki/Your_Company]",
    "[REPLACE: https://www.wikidata.org/wiki/Q12345]",
    "[REPLACE: https://www.linkedin.com/company/your-company]",
    "[REPLACE: https://www.youtube.com/@yourchannel]",
    "[REPLACE: https://www.crunchbase.com/organization/your-company]",
    "[REPLACE: https://twitter.com/yourcompany]",
    "[REPLACE: https://github.com/yourcompany]"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "[REPLACE: +1-555-000-0000]",
    "contactType": "customer service",
    "email": "[REPLACE: support@yoursite.com]"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[REPLACE: 123 Main St]",
    "addressLocality": "[REPLACE: City]",
    "addressRegion": "[REPLACE: State]",
    "postalCode": "[REPLACE: 12345]",
    "addressCountry": "[REPLACE: US]"
  }
}
```

## Local Business

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[REPLACE: Business Name]",
  "url": "[REPLACE: https://yoursite.com]",
  "image": "[REPLACE: https://yoursite.com/storefront.jpg]",
  "telephone": "[REPLACE: +1-555-000-0000]",
  "priceRange": "[REPLACE: $$]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[REPLACE: 123 Main St]",
    "addressLocality": "[REPLACE: City]",
    "addressRegion": "[REPLACE: State]",
    "postalCode": "[REPLACE: 12345]",
    "addressCountry": "[REPLACE: US]"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "[REPLACE: 37.7749]",
    "longitude": "[REPLACE: -122.4194]"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  ],
  "sameAs": [
    "[REPLACE: Google Business Profile URL]",
    "[REPLACE: Yelp URL]",
    "[REPLACE: LinkedIn URL]"
  ]
}
```

## Article with Author (E-E-A-T)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[REPLACE: Article Title]",
  "description": "[REPLACE: Brief article summary, under 160 characters]",
  "image": "[REPLACE: https://yoursite.com/article-image.jpg]",
  "datePublished": "[REPLACE: 2026-01-15T08:00:00+00:00]",
  "dateModified": "[REPLACE: 2026-02-01T10:30:00+00:00]",
  "author": {
    "@type": "Person",
    "name": "[REPLACE: Author Name]",
    "url": "[REPLACE: https://yoursite.com/team/author-name]",
    "jobTitle": "[REPLACE: Senior Engineer]",
    "worksFor": {
      "@type": "Organization",
      "name": "[REPLACE: Your Company]"
    },
    "sameAs": [
      "[REPLACE: https://linkedin.com/in/author]",
      "[REPLACE: https://twitter.com/author]"
    ]
  },
  "publisher": {
    "@type": "Organization",
    "name": "[REPLACE: Your Company]",
    "logo": {
      "@type": "ImageObject",
      "url": "[REPLACE: https://yoursite.com/logo.png]"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "[REPLACE: https://yoursite.com/blog/article-slug]"
  },
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".article-summary", ".key-findings"]
  }
}
```

## Software / SaaS Application

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "[REPLACE: Your Product Name]",
  "applicationCategory": "[REPLACE: BusinessApplication]",
  "operatingSystem": "Web",
  "url": "[REPLACE: https://yoursite.com]",
  "description": "[REPLACE: What your product does, 1-2 sentences]",
  "offers": {
    "@type": "Offer",
    "price": "[REPLACE: 29.00]",
    "priceCurrency": "USD",
    "priceValidUntil": "[REPLACE: 2026-12-31]"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[REPLACE: 4.5]",
    "reviewCount": "[REPLACE: 150]"
  }
}
```

## Product (E-commerce)

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "[REPLACE: Product Name]",
  "image": "[REPLACE: https://yoursite.com/product.jpg]",
  "description": "[REPLACE: Product description]",
  "brand": {
    "@type": "Brand",
    "name": "[REPLACE: Brand Name]"
  },
  "offers": {
    "@type": "Offer",
    "url": "[REPLACE: https://yoursite.com/product/slug]",
    "price": "[REPLACE: 49.99]",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "priceValidUntil": "[REPLACE: 2026-12-31]"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[REPLACE: 4.2]",
    "reviewCount": "[REPLACE: 89]"
  }
}
```

## WebSite with SearchAction

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "[REPLACE: Your Site Name]",
  "url": "[REPLACE: https://yoursite.com]",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "[REPLACE: https://yoursite.com/search?q={search_term_string}]"
    },
    "query-input": "required name=search_term_string"
  }
}
```

## Implementation Notes

1. **Server-render all schemas** — AI crawlers (GPTBot, ClaudeBot) do NOT execute JavaScript
2. **Place in `<head>`** inside `<script type="application/ld+json">` tags
3. **One schema per script tag** — multiple blocks are fine
4. **sameAs is the #1 GEO priority** — link to Wikipedia, Wikidata, LinkedIn, YouTube minimum
5. **speakable marks AI-ready content** — add to Article schemas on key pages
6. **Validate at** https://validator.schema.org/ before deploying
