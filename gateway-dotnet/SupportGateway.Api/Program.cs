using System.Net.Http.Json;
using System.Text.Json;
using Microsoft.EntityFrameworkCore;
using SupportGateway.Api.Data;

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

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

var app = builder.Build();
app.UseCors();

// Proxy: POST /api/chat -> Python /chat
// Proxy: POST /api/chat -> Python /chat
app.MapPost("/api/chat", async (HttpContext context, IHttpClientFactory factory) =>
{
    var client = factory.CreateClient("Python");
    var body = await context.Request.ReadFromJsonAsync<ChatRequest>();
    if (body?.Message == null)
        return Results.BadRequest(new { detail = "message required" });
    var payload = new
    {
        message = body.Message,
        user_id = body.UserId,
        channel = body.Channel,
        history = body.History
    };
    var response = await client.PostAsJsonAsync("/chat", payload);
    if (!response.IsSuccessStatusCode)
        return Results.Json(new { detail = await response.Content.ReadAsStringAsync() }, statusCode: (int)response.StatusCode);
    var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
    var data = await response.Content.ReadFromJsonAsync<ChatResponse>(options);
    return Results.Ok(data);
});

// POST: guarda conversaci�n en SQLite
app.MapPost("/api/conversations/log", async (ConversationLogRequest req, AppDbContext db) =>
{
    db.ConversationLogs.Add(new ConversationLog
    {
        UserId = req.UserId,
        Channel = req.Channel,
        Message = req.Message,
        Response = req.Response,
        Summary = req.Summary,
        At = DateTime.UtcNow
    });
    await db.SaveChangesAsync();
    return Results.Ok(new { ok = true });
});

// GET: devuelve todas las conversaciones desde la base
app.MapGet("/api/conversations/log", async (AppDbContext db) =>
{
    var list = await db.ConversationLogs
        .OrderByDescending(x => x.At)
        .ToListAsync();
    return Results.Ok(list);
});

app.Run();

// DTOs
record ChatMessage(string Role, string Content);
record ChatRequest(string? UserId, string Message, string? Channel, List<ChatMessage>? History);
record ChatResponse(string Answer, object? Sources, string? Summary);
record ConversationLogRequest(string? UserId, string? Channel, string? Message, string? Response, string? Summary);