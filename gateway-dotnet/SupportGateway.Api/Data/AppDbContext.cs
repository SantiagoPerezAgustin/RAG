using Microsoft.EntityFrameworkCore;

namespace SupportGateway.Api.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
        public DbSet<ConversationLog> ConversationLogs { get; set; }
    }
}
