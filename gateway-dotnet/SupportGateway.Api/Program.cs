using System.Net.Http.Json;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHttpClient("Python", (sp, client) =>
{
    var baseUrl = builder.Configuration["AiService:BaseUrl"] ?? "http://127.0.0.1:8000";
    client.BaseAddress = new Uri(baseUrl);
    client.DefaultRequestHeaders.TryAddWithoutValidation("Accept", "application/json");
});
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.WithOrigins("http://localhost:5173")
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();
app.UseCors();

// Proxy: POST /api/chat -> Python /chat
app.MapPost("/api/chat", async (HttpContext context, IHttpClientFactory factory) =>
{
    var client = factory.CreateClient("Python");
    var body = await context.Request.ReadFromJsonAsync<ChatRequest>();
    if (body?.Message == null)
        return Results.BadRequest(new { detail = "message required" });

    var response = await client.PostAsJsonAsync("/chat", new { message = body.Message, user_id = body.UserId, channel = body.Channel });
    if (!response.IsSuccessStatusCode)
        return Results.Json(new { detail = await response.Content.ReadAsStringAsync() }, statusCode: (int)response.StatusCode);

    var data = await response.Content.ReadFromJsonAsync<ChatResponse>();
    return Results.Ok(data);
});

// Log de conversación (por ahora en memoria; después podés reemplazar por SQL Server)
var conversationLog = new List<ConversationLogEntry>();
app.MapPost("/api/conversations/log", (ConversationLogRequest req) =>
{
    conversationLog.Add(new ConversationLogEntry(
        req.UserId,
        req.Channel,
        req.Message,
        req.Response,
        req.Summary,
        DateTime.UtcNow
    ));
    return Results.Ok(new { ok = true });
});

app.Run();

// DTOs
record ChatRequest(string? UserId, string Message, string? Channel);
record ChatResponse(string Answer, object? Sources, string? Summary);
record ConversationLogRequest(string? UserId, string? Channel, string? Message, string? Response, string? Summary);
record ConversationLogEntry(string? UserId, string? Channel, string? Message, string? Response, string? Summary, DateTime At);