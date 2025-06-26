from fastapi.middleware.cors import CORSMiddleware

def configure_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # altere para domínios específicos em produção
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )