---
title: Senior Java
name: senior-java
namespace: stringhub
type: app
version: 0.1.0
description: World-class Java and Spring Boot development skill for enterprise applications, microservices, and cloud-native systems. Expertise in Spring Framework, Spring Boot 3.x, Spring Cloud, JPA/Hibernate, and reactive programming with WebFlux. Includes project scaffolding, dependency management, security implementation, and performance optimization.
tags: [java, spring-boot, microservices, jpa, security]
---

# Senior Java

Java / Spring Boot development helpers. Each action runs a bundled Python generator
that emits production-ready Spring Boot 3.x code, config, or analysis — call the action
instead of writing the code yourself. Each generator emits a *different* artifact: a whole
project vs. one entity stack vs. CRUD endpoints vs. a security config vs. an analysis report.

**How flags reach the generator:** the first String field is the generator's required
positional/named arg (shown below); **every other flag goes in `extra_args` as ONE
space-separated string** (e.g. `extra_args` = `--type microservice --db postgresql`). All
flags below are the generator's real flags. Optionals shown as `[--flag <type>]` with their
default. Generators print to stdout by default; pass `--output`/`-o` to write files, `--json`
for JSON, `--verbose`/`-v` for detail.
**Passthrough gotcha:** a value in `extra_args` cannot begin with `--` (the splitter treats it
as a new flag). All flags below take normal values, so this only bites if you invent one.

## Scaffold / generate (output goes to stdout unless `--output`/`-o <dir>`)
- **`/act.spring_project_scaffolder`** `--name <kebab-case>` (String field) — full Spring Boot 3.x
  project (layered architecture, Docker, CI/CD). extra_args: `[--type microservice|monolith|reactive]`
  (default `microservice`) `[--db postgresql|mysql|mongodb|h2]` (default `postgresql`)
  `[--security jwt|oauth2|basic]` `[--java 17|21]` (default `17`) `[--group-id <id>]`
  (default `com.example`) `[--output <dir>]` (default `.`) `[--no-docker]` `[--no-ci]` `[--verbose]` `[--json]`.
- **`/act.entity_generator`** `--name <PascalCase>` `--fields "<id:Long,name:String,...>"` (both String
  fields) — JPA entity stack (entity + repository + service + controller + DTO/mapper). extra_args:
  `[--relations "<field:ManyToOne,...>"]` `[--package <pkg>]` (default `com.example`) `[--output <dir>]`
  (default `.`) `[--auditable]` `[--soft-delete]` `[--verbose]` `[--json]`.
- **`/act.api_endpoint_generator`** `--resource <name>` (String field) — REST CRUD endpoints. extra_args:
  `[--methods <GET,POST,PUT,DELETE>]` (default all four) `[--paginated]` `[--package <pkg>]`
  (default `com.example`) `[--output <file>]` `[--json]`.
- **`/act.security_config_generator`** `--type jwt|oauth2` (String field, required) — Spring Security
  config (roles, filter chain, method security). extra_args: `[--roles <ADMIN,USER>]` (default
  `ADMIN,USER`) `[--issuer-uri <url>]` (required for `oauth2`) `[--package <pkg>]` (default
  `com.example`) `[--output <dir>]` `[--json]`.

## Analyze (point at real source/build files)
- **`/act.dependency_analyzer`** `--file <pom.xml|build.gradle>` (String field) — outdated/vulnerable
  deps + upgrade paths. extra_args: `[--check-security]` `[--output <file>]` (md or json by extension)
  `[--json]` `[--verbose]`.
- **`/act.performance_profiler`** — N+1 queries / JVM bottlenecks + optimization recommendations.
  All flags via extra_args: `[--analyze-queries <DIR>]` `[--output <file>]` `[--json]` `[--verbose]`.

Deep-reference docs are bundled under `references/` (Spring Boot best practices,
microservices patterns, JPA/Hibernate, Spring Security, performance tuning) — the flags
above are complete, so you shouldn't need them.

```act.spring_project_scaffolder
CLI ./scripts/_argshim.sh ./scripts/spring_project_scaffolder.py "{name}" "{extra_args}"
  name: string (required) "Project name (kebab-case), e.g. order-service"
  extra_args: string (optional) "Raw extra flags, e.g. --type microservice --db postgresql --security jwt" = ""
```

```act.entity_generator
CLI ./scripts/_argshim.sh ./scripts/entity_generator.py "{name}" --fields "{fields}" "{extra_args}"
  name: string (required) "Entity name (PascalCase), e.g. Product"
  fields: string (required) "Field spec, e.g. id:Long,name:String,price:BigDecimal"
  extra_args: string (optional) "Raw extra flags, e.g. --relations customer:ManyToOne --auditable" = ""
```

```act.dependency_analyzer
CLI ./scripts/_argshim.sh ./scripts/dependency_analyzer.py "{file}" "{extra_args}"
  file: string (required) "Path to pom.xml or build.gradle"
  extra_args: string (optional) "Raw extra flags, e.g. --check-security --output report.md" = ""
```

```act.api_endpoint_generator
CLI ./scripts/_argshim.sh ./scripts/api_endpoint_generator.py "{resource}" "{extra_args}"
  resource: string (required) "Resource name, e.g. order, product"
  extra_args: string (optional) "Raw extra flags, e.g. --methods GET,POST,PUT,DELETE --paginated" = ""
```

```act.security_config_generator
CLI ./scripts/_argshim.sh ./scripts/security_config_generator.py --type "{type}" "{extra_args}"
  type: string (required) "Security type: jwt or oauth2"
  extra_args: string (optional) "Raw extra flags, e.g. --roles ADMIN,USER --issuer-uri https://auth.example.com" = ""
```

```act.performance_profiler
CLI ./scripts/_argshim.sh ./scripts/performance_profiler.py "{extra_args}"
  extra_args: string (optional) "Raw flags, e.g. --analyze-queries src/ --output performance-report.md" = ""
```
