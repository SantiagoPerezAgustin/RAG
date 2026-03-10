using Microsoft.EntityFrameworkCore;

namespace SupportGateway.Api.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
        public DbSet<ConversationLog> ConversationLogs { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Tipos correctos para SQL Server (evitan error datetime2 vs text y ntext)
            modelBuilder.Entity<ConversationLog>(e =>
            {
                e.Property(x => x.At).HasColumnType("datetime2");
                e.Property(x => x.UserId).HasColumnType("nvarchar(max)");
                e.Property(x => x.Channel).HasColumnType("nvarchar(max)");
                e.Property(x => x.Message).HasColumnType("nvarchar(max)");
                e.Property(x => x.Response).HasColumnType("nvarchar(max)");
                e.Property(x => x.Summary).HasColumnType("nvarchar(max)");
            });
        }
    }
}
