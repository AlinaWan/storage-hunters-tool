# Præstantia Summa 2 Design Handbook

**Version 1**

---

# i. General Design Principles

The core architectural and design style should align as much as possible with the [**Framework Design Guidelines (Third Edition)**](https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/). Developers are encouraged to [order](https://www.informit.com/store/framework-design-guidelines-conventions-idioms-and-9780135896464) a physical or digital copy of the handbook and familiarize themselves with the principles described within.

Consistency is one of the primary goals of this handbook. The standards defined here are intended to improve readability, maintainability, discoverability, and tooling support across the entire codebase.

---

# ii. Documentation Standards

## ii.i. Python

All public APIs and classes written in Python should be documented using XML-style tags as recommended by [*Recommended XML tags for C# documentation comments*](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/recommended-tags).

### Style

* Tags must be written within a docstring.
* The opening and closing marks should always be placed on their own lines, with the content written in between.
* Do not indent the text content within these tags.

### Example

```python
"""
<summary>
The summary goes here. Also see: <see cref="Important.for_context"/>.
</summary>
"""
```

---

# § 1. Naming Conventions

Consistency in naming is crucial for readability and tooling support. Please follow the language-specific conventions outlined below.

### § 1.0. General Naming Principles

* **Clarity Over Brevity:** Names should prioritize precision over brevity. Prefer precise and descriptive class, method, and variable names that clearly communicate their purpose, even when they are longer.
* **Describe What Something Is:** Names should describe what an object represents or the responsibility it fulfills, rather than how it is implemented.
* **Use Correct Grammar:** Classes, structs, and records should be named using nouns or noun phrases. Methods should be named using verbs or verb phrases that describe the action they perform.
* **Prefer Suffixes Over Prefixes:** When additional semantic information is required, prefer suffixes over prefixes. For example, prefer `DiscordWebhookLoggerPayloadFormatter` over `FormatterDiscordWebhookLoggerPayload`, and `ConsoleLoggerProvider` over `ProviderConsoleLogger`.
* **Avoid Abbreviations:** Avoid abbreviations and acronyms unless they are universally understood or already established within the project. Prefer complete words that improve readability and remove ambiguity.

**Examples**

| Preferred                                     | Avoid               |
| --------------------------------------------- | ------------------- |
| `GreatestCommonDivisor`                       | `Gcd`               |
| `Process`                                     | `Proc`              |
| `FullyQualifiedName`                          | `Fqn`               |
| `instantiate_class_from_fully_qualified_name` | `instantiate_class` |
| `DiscordWebhookLoggerPayloadFormatter`        | `DiscordFormatter`  |
| `FileWatcher`                                 | `Watcher`           |
| `ResourceManager`                             | `Manager`           |

## § 1.1. Python

* **Case:** `snake_case` for functions, variables, and methods; `PascalCase` for classes (as defined in [PEP 8](https://peps.python.org/pep-0008/#naming-conventions)).
* **File Name:** `snake_case` for file names.
* **File-to-Class Mapping:** File names must match the name of the primary class they contain, adjusted for standard naming case differences (e.g., `console_logger_provider.py` must contain the class `ConsoleLoggerProvider`). We strictly enforce a one-class-per-file rule; multiple classes are only permitted in a single file if they are strictly necessary to support the purpose of the primary class (such as a class created to hold Enums).
* **Interfaces:** All abstractions must be be defined using `typing.Protocol` to enforce structural typing and ensure proper interface adherence throughout the codebase. By convention, all interface names must follow Hungarian notation using the `I` prefix (e.g., `IDisposable`).

## § 1.2. C++

* **Case:** `PascalCase` for classes, structs, and methods.
* **File Name:** `PascalCase` for file names.

## § 1.3. Assembly (x86-64 Windows / MASM)

* **Case:** `snake_case` for labels, procedures, and variables.
* **File Name:** `snake_case` for file names.

## § 1.4. Dynamic Link Libraries (DLLs)

Naming conventions for DLLs depend on the project structure to avoid namespace collisions and improve discoverability.

### Multiple-File Source DLLs (large libraries)

Use `flatcase` (all lowercase, no separators). This is used when a library provides a broad suite of related utilities or a complex interface where the library name is distinct from individual source modules (e.g., `toolvision.dll`).

### Single-File Source DLLs

These should match the primary source file name exactly, regardless of the case used in the source (e.g., `MathEngine.cpp` → `MathEngine.dll`).

---

# § 2. Python Coding Standards

## § 2.1. Structural Requirements

* **Encapsulation:** To maintain a strictly object-oriented structure, all methods must be defined within a class. Top-level functions are not permitted, even for static methods or modules containing a single method. Any modules created solely to hold global variables (such as a Constants class or data transfer object) must also have those variables encapsulated within a class.
* **Static Method Restrictions:** Static methods are not permitted to perform any logging operations. To maintain clear separation of concerns, static methods should instead return a result represented by an `Enum` value if the caller must know the specific result. The caller is solely responsible for determining how to handle or log that result.

## § 2.2. Type System

To promote maintainability and clarity, please adhere to the following type-aliasing and decoration standards.

* **Void Methods:** Use `typing.Callable` for function signatures (aliased as **Action**) when the return type is `None`.
* **Dictionaries:** Always use `typing.Dict` (aliased as **Dictionary**) instead of the built-in `dict` type to maintain a consistent naming convention throughout the type system.
* **Sealed Classes:** By default, all classes should be considered sealed. Use the `@typing.final` decorator (aliased as **@sealed**) on any class that is not explicitly designed for inheritance.
* **Read-Only Values:** Use `typing.Final` (aliased as **ReadOnly**) for any variable or attribute that is intended to be immutable after initialization.

### Example Implementation

```python
from typing import Callable as Action, Dict as Dictionary, Final as ReadOnly, final as sealed

@sealed
class DataProcessor:
    configuration: ReadOnly[Dictionary[str, str]] = {"mode": "default"}

    def execute(self, callback: Action) -> None:
        callback()
```

---

# § 3. Resource Management & Threading

## § 3.1. Resource Management

* **Disposable Pattern:** Prefer the `IDisposable` interface (via `typing.Protocol`) over `__enter__`/`__exit__` methods. A `dispose` method must be implemented to clear state. It is strongly encouraged to also include a `stop`, and if applicable, a `close` method with distinct responsibility. If a `stop` or `close` method is applicable to the resource, the `dispose` method must invoke these before clearing the state.
* **Process Exit Handling:** If a module requires specific actions to be performed upon process termination, register the logic via `atexit`. By convention, these methods should be named `current_domain_process_exit`.

## § 3.2. Threading & Synchronization

* **Synchronization:** Use a threading event for lifecycle control, which by convention must be named `_cts`.
* **Low-Level Handles:** For synchronization primitives, utilize `WaitForSingleObject` and `WaitForMultipleObjects`. All handle variables must follow Hungarian notation. Use **camelCase** for native method handles (e.g., `hEvent` or `hDir`), while handles resulting from `CreateEvent` must use **snake_case** with an `h` prefix (e.g., `h_event`, `h_overlapped_event`, or `_h_stop_event`).

---

# § 4. Architectural Standards

The use of the factory-provider-handler-formatter pattern should be followed across modules.

This pattern is fundamental to our architecture, as it leverages Inversion of Control (IoC) to decouple object creation from usage, and adheres to the Open/Closed Principle (OCP) by allowing the engine to be extended without modifying existing source code.
