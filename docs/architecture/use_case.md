## UseCase Patterns

### UseCase (without PK)
Used for operations on collections:
- Creation (POST /resource/)
- Getting a list (GET /resource/)
- Mass operations

### DetailUseCase (with PK)  
Used for operations on a specific entity:
- Reading (GET /resource/{pk}/)
- Update (POST/PUT /resource/{pk}/)
- Delete (DELETE /resource/{pk}/)